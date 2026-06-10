import json
import logging
from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session

from backend.app.models import Conversation, Scheme, UserDocument, Message
from backend.app.config import SCHEMES_FILE_PATH
from backend.app.agents.interview import InterviewAgent
from backend.app.agents.profiler import ProfilerAgent
from backend.app.agents.eligibility import EligibilityAgent
from backend.app.agents.rag import RetrievalAgent
from backend.app.agents.document_intel import DocumentGapAgent, ActionPlanAgent

logger = logging.getLogger(__name__)

# Cache loaded schemes list
_cached_schemes: List[Dict[str, Any]] = []

def get_all_schemes_list(db: Session) -> List[Dict[str, Any]]:
    """
    Loads all schemes from the database, falling back to schemes_data.json if DB is empty.
    Caches the list for speed.
    """
    global _cached_schemes
    if _cached_schemes:
        return _cached_schemes
        
    db_schemes = db.query(Scheme).all()
    if db_schemes:
        list_schemes = []
        for s in db_schemes:
            list_schemes.append({
                "scheme_id": s.id,
                "scheme_name": s.name,
                "ministry": s.ministry,
                "state": s.state,
                "eligibility_rules": json.loads(s.eligibility_rules),
                "benefits": json.loads(s.benefits),
                "required_documents": json.loads(s.required_documents),
                "application_steps": json.loads(s.application_steps),
                "official_link": s.official_link,
                "faqs": json.loads(s.faqs)
            })
        _cached_schemes = list_schemes
        return list_schemes
        
    # Fallback to file reading
    try:
        with open(SCHEMES_FILE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Seed the database
            for s_data in data:
                db_scheme = Scheme(
                    id=s_data["scheme_id"],
                    name=s_data["scheme_name"],
                    ministry=s_data["ministry"],
                    state=s_data["state"],
                    eligibility_rules=json.dumps(s_data["eligibility_rules"]),
                    benefits=json.dumps(s_data["benefits"]),
                    required_documents=json.dumps(s_data["required_documents"]),
                    application_steps=json.dumps(s_data["application_steps"]),
                    official_link=s_data["official_link"],
                    faqs=json.dumps(s_data.get("faqs", []))
                )
                db.add(db_scheme)
            db.commit()
            _cached_schemes = data
            return data
    except Exception as e:
        logger.error(f"Error seeding schemes: {e}")
        return []

class AgentCoordinator:
    def __init__(self, db: Session, language: str = "English"):
        self.db = db
        self.language = language
        self.schemes = get_all_schemes_list(db)
        
        # Instantiate agents
        self.interview_agent = InterviewAgent(language=self.language)
        self.profiler_agent = ProfilerAgent()
        self.eligibility_agent = EligibilityAgent()
        self.rag_agent = RetrievalAgent(self.schemes)
        self.doc_gap_agent = DocumentGapAgent()
        self.action_plan_agent = ActionPlanAgent()

    def process_message(self, conversation_id: str, message_text: str) -> Dict[str, Any]:
        """
        Coordinates the conversation step:
        1. Checks current state.
        2. If user answers a question, profiles it.
        3. Looks for RAG informational queries and handles side queries.
        4. Finds the next question.
        5. If completed, computes full eligibility, document gap, and action plans.
        """
        conv = self.db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if not conv:
            raise ValueError("Conversation not found")

        profile = json.loads(conv.current_profile)
        
        # Ensure we sync user's available documents list into their profile dictionary
        user_docs = self.db.query(UserDocument).filter(UserDocument.user_id == conv.user_id).all()
        available_docs = [ud.document_name for ud in user_docs if ud.is_available]
        profile["available_documents"] = available_docs
        
        # Check what was the last question we asked the user
        last_msg = self.db.query(Message).filter(
            Message.conversation_id == conversation_id,
            Message.sender == "assistant"
        ).order_by(Message.created_at.desc()).first()

        last_question_field = None
        if last_msg:
            # Match prompt text to identify the field we asked
            from backend.app.agents.interview import QUESTIONS
            for q in QUESTIONS:
                prompts = q["prompts"]
                if last_msg.text in prompts.values() or any(p in last_msg.text for p in prompts.values()):
                    last_question_field = q["field"]
                    break

        # 1. Profile extraction (if user has sent a reply to a specific question)
        rag_answer = None
        if last_question_field and message_text:
            extracted_val = self.profiler_agent.extract_value(last_question_field, message_text)
            if extracted_val is not None:
                if last_question_field == "available_documents" and isinstance(extracted_val, list):
                    # Save user documents in the UserDocuments table
                    # First clear old entries and populate new ones
                    self.db.query(UserDocument).filter(UserDocument.user_id == conv.user_id).delete()
                    for doc_name in extracted_val:
                        self.db.add(UserDocument(user_id=conv.user_id, document_name=doc_name, is_available=True))
                    self.db.commit()
                    profile["available_documents"] = extracted_val
                else:
                    profile[last_question_field] = extracted_val
                
                # Save updated profile
                conv.current_profile = json.dumps(profile)
                self.db.commit()

        # 2. RAG Side-Query Check
        # If the user's message looks like an informational query (e.g. contains "what is", "kya hai", "benefits", "?"),
        # run the retrieval agent to find scheme FAQs.
        # This allows citizens to ask questions mid-interview without breaking flow.
        query_indicators = ["what", "kya", "how", "kab", "kaise", "scheme", "benefit", "fayda", "?", "faq", "mili"]
        clean_msg = message_text.lower()
        if any(ind in clean_msg for ind in query_indicators) and len(clean_msg.split()) > 2:
            search_results = self.rag_agent.search(message_text, top_k=1)
            if search_results:
                top_match = search_results[0]
                if top_match["type"] == "faq":
                    rag_answer = f"[💡 Informational Answer regarding {top_match['scheme_name']}]:\nQ: {top_match['title']}\nA: {top_match['content']}\n\nOfficial Link: {top_match['official_link']}"
                else:
                    rag_answer = f"[💡 Scheme Info for {top_match['scheme_name']}]:\n{top_match['content']}\n\nOfficial Link: {top_match['official_link']}"

        # 3. Determine next question
        next_q = self.interview_agent.get_next_question(profile)
        
        # Limit check
        conv.question_count += 1
        if conv.question_count >= 20 or next_q is None:
            # Mark assessment as completed
            conv.status = "completed"
            self.db.commit()
            
            # Execute final matching pipeline
            evaluation = self.eligibility_agent.evaluate_all_schemes(profile, self.schemes)
            
            # Extract eligible schemes
            eligible_list = evaluation["Highly Eligible"] + evaluation["Eligible"] + evaluation["Potentially Eligible"]
            
            # Run gap analysis
            # Collate required documents for eligible schemes
            all_req_docs = set()
            for s in eligible_list:
                all_req_docs.update(s.get("required_documents", []))
            
            doc_analysis = self.doc_gap_agent.analyze_documents(list(all_req_docs), profile.get("available_documents", []))
            
            # Generate action plan
            action_plan = self.action_plan_agent.generate_plan(doc_analysis["missing"], eligible_list)
            
            results = {
                "profile": profile,
                "eligibility_results": evaluation,
                "document_analysis": doc_analysis,
                "action_plan": action_plan
            }
            
            if self.language == "Hindi":
                from backend.app.utils.translator import translate_results_to_hindi
                results = translate_results_to_hindi(results)
            
            # Save final message from assistant
            final_message_text = "Congratulations! Your eligibility assessment is complete. I have generated your welfare dashboard and a personalized action plan. Please check the results below."
            if self.language == "Hindi":
                final_message_text = "बधाई हो! आपका पात्रता मूल्यांकन पूरा हो गया है। मैंने आपका कल्याण डैशबोर्ड और एक व्यक्तिगत कार्य योजना तैयार की है। कृपया नीचे परिणाम देखें।"
            elif self.language == "Hinglish":
                final_message_text = "Congratulations! Aapka eligibility assessment complete ho gaya hai. Maine aapke liye dashboard aur action plan generate kar diya hai. Please neeche results check karein."
                
            assistant_msg = Message(
                conversation_id=conversation_id,
                sender="assistant",
                text=final_message_text
            )
            self.db.add(assistant_msg)
            self.db.commit()
            
            return {
                "is_completed": True,
                "next_question": None,
                "question_count": conv.question_count,
                "results": results,
                "assistant_message": {
                    "id": assistant_msg.id,
                    "sender": "assistant",
                    "text": assistant_msg.text,
                    "created_at": assistant_msg.created_at.isoformat()
                }
            }

        # Save the new question message to the DB
        prompt_text = next_q["text"]
        # Prepend the RAG response if we found a side answer
        response_text = prompt_text
        if rag_answer:
            response_text = f"{rag_answer}\n\n-------------------------\nNow, continuing the eligibility assessment:\n{prompt_text}"
            
        assistant_msg = Message(
            conversation_id=conversation_id,
            sender="assistant",
            text=response_text
        )
        self.db.add(assistant_msg)
        self.db.commit()
        
        return {
            "is_completed": False,
            "next_question": prompt_text,
            "question_count": conv.question_count,
            "results": None,
            "assistant_message": {
                "id": assistant_msg.id,
                "sender": "assistant",
                "text": assistant_msg.text,
                "created_at": assistant_msg.created_at.isoformat()
            }
        }
