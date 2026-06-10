import os
import json
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import Dict, Any, List

from backend.app.database import get_db
from backend.app.models import User, Conversation, Message, Report
from backend.app.auth import get_current_user
from backend.app.schemas import StartChatRequest, StartChatResponse, MessageRequest, MessageAnswerResponse, MessageResponse
from backend.app.agents.coordinator import AgentCoordinator

router = APIRouter(prefix="/api/chat", tags=["chat"])

@router.post("/start", response_model=StartChatResponse)
def start_chat(req: StartChatRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Initializes a new assessment conversation.
    """
    # Create new conversation
    lang = req.preferred_language or current_user.preferred_language
    conv = Conversation(
        user_id=current_user.id,
        status="active",
        current_profile="{}",
        question_count=0
    )
    db.add(conv)
    db.commit()
    db.refresh(conv)
    
    # Initialize coordinator to ask the first question
    coordinator = AgentCoordinator(db, language=lang)
    result = coordinator.process_message(conv.id, "")
    
    return StartChatResponse(
        conversation_id=conv.id,
        status="active",
        message="Assessment started.",
        next_question=result["next_question"],
        question_count=result["question_count"],
        is_completed=result["is_completed"]
    )

@router.post("/message", response_model=MessageAnswerResponse)
def post_message(req: MessageRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Submits user message and returns the next question or the final welfare assessment report.
    """
    conv = db.query(Conversation).filter(Conversation.id == req.conversation_id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation session not found")
        
    # Save user message to database
    user_msg = Message(
        conversation_id=conv.id,
        sender="user",
        text=req.text
    )
    db.add(user_msg)
    db.commit()
    db.refresh(user_msg)
    
    # Run agent pipeline
    coordinator = AgentCoordinator(db, language=current_user.preferred_language)
    agent_res = coordinator.process_message(conv.id, req.text)
    
    # Structure response
    assistant_msg_data = MessageResponse(
        id=agent_res["assistant_message"]["id"],
        sender=agent_res["assistant_message"]["sender"],
        text=agent_res["assistant_message"]["text"],
        created_at=datetime.fromisoformat(agent_res["assistant_message"]["created_at"])
    )
    
    return MessageAnswerResponse(
        message=assistant_msg_data,
        next_question=agent_res["next_question"],
        question_count=agent_res["question_count"],
        is_completed=agent_res["is_completed"],
        results=agent_res["results"]
    )

@router.get("/history/{conversation_id}", response_model=List[MessageResponse])
def get_chat_history(conversation_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Returns the message history for a given conversation.
    """
    conv = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()
    
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
        
    messages = db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.created_at.asc()).all()
    return messages

@router.get("/report/{conversation_id}/download")
def download_pdf_report(conversation_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Generates and downloads the personalized action plan PDF report.
    """
    conv = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()
    
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation session not found")
        
    if conv.status != "completed":
        raise HTTPException(status_code=400, detail="Cannot generate report for an active/uncompleted assessment")

    # Generate directories
    reports_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "reports")
    os.makedirs(reports_dir, exist_ok=True)
    pdf_filename = os.path.join(reports_dir, f"report_{conversation_id}.pdf")

    # Run coordinator evaluation to get full fresh data
    coordinator = AgentCoordinator(db, language=current_user.preferred_language)
    profile = json.loads(conv.current_profile)
    
    evaluation = coordinator.eligibility_agent.evaluate_all_schemes(profile, coordinator.schemes)
    eligible_list = evaluation["Highly Eligible"] + evaluation["Eligible"] + evaluation["Potentially Eligible"]
    
    doc_analysis = coordinator.doc_gap_agent.analyze_documents(
        list(set(d for s in eligible_list for d in s.get("required_documents", []))),
        profile.get("available_documents", [])
    )
    action_plan = coordinator.action_plan_agent.generate_plan(doc_analysis["missing"], eligible_list)
    
    results = {
        "eligibility_results": evaluation,
        "document_analysis": doc_analysis,
        "action_plan": action_plan
    }

    if current_user.preferred_language == "Hindi":
        from backend.app.utils.translator import translate_results_to_hindi
        results = translate_results_to_hindi(results)

    # Generate PDF
    from backend.app.utils.pdf_generator import generate_eligibility_pdf
    generate_eligibility_pdf(pdf_filename, profile, results, current_user.preferred_language)
    
    # Save Report record in DB
    report_record = db.query(Report).filter(Report.conversation_id == conversation_id).first()
    if not report_record:
        report_record = Report(conversation_id=conversation_id, pdf_path=pdf_filename)
        db.add(report_record)
        db.commit()

    return FileResponse(
        pdf_filename,
        media_type="application/pdf",
        filename=f"JanMitra_Eligibility_Report_{current_user.full_name.replace(' ', '_')}.pdf"
    )
