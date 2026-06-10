import re
import json
import logging
from typing import Dict, Any, List, Optional
from backend.app.config import OPENAI_API_KEY

logger = logging.getLogger(__name__)

# Fallback values mapping
OCCUPATION_MAP = {
    "farmer": "Farmer", "kisan": "Farmer", "kheti": "Farmer", "कृषि": "Farmer", "किसान": "Farmer",
    "student": "Student", "pupil": "Student", "college": "Student", "padhai": "Student", "छात्र": "Student", "विद्यार्थी": "Student",
    "business": "Business Owner", "dukan": "Business Owner", "shop": "Business Owner", "dhandha": "Business Owner", "व्यापारी": "Business Owner", "startup": "Startup Founder",
    "unemployed": "Unemployed", "jobless": "Unemployed", "berojgar": "Unemployed", "बेरोजगार": "Unemployed",
    "salaried": "Salaried", "job": "Salaried", "naukri": "Salaried", "service": "Salaried", "नौकरी": "Salaried"
}

CATEGORY_MAP = {
    "general": "General", "gen": "General", "सामान्य": "General",
    "obc": "OBC", "ओबीसी": "OBC", "backward": "OBC",
    "sc": "SC", "scheduled caste": "SC", "अनुसूचित जाति": "SC",
    "st": "ST", "scheduled tribe": "ST", "अनुसूचित जनजाति": "ST",
    "ews": "EWS", "economically weaker": "EWS"
}

STATE_MAP = {
    "madhya pradesh": "Madhya Pradesh", "mp": "Madhya Pradesh", "मदद": "Madhya Pradesh", "मध्य प्रदेश": "Madhya Pradesh",
    "uttar pradesh": "Uttar Pradesh", "up": "Uttar Pradesh", "उत्तर प्रदेश": "Uttar Pradesh",
    "haryana": "Haryana", "हरियाणा": "Haryana",
    "delhi": "Delhi", "दिल्ली": "Delhi",
    "bihar": "Bihar", "बिहार": "Bihar",
    "rajasthan": "Rajasthan", "राजस्थान": "Rajasthan",
    "maharashtra": "Maharashtra", "महाराष्ट्र": "Maharashtra",
    "punjab": "Punjab", "पंजाब": "Punjab",
    "gujarat": "Gujarat", "गुजरात": "Gujarat"
}

DOCUMENT_KEYWORDS = {
    "Aadhaar Card": ["aadhaar", "adhar", "आधार", "uid"],
    "Ration Card": ["ration", "राशन", "rashan"],
    "Bank Passbook": ["bank", "passbook", "pass book", "खाता", "बैंक"],
    "Land Record": ["land", "record", "khasra", "khatauni", "जमीन", "patta", "ownership"],
    "Samagra ID": ["samagra", "समग्र"],
    "Domicile Certificate": ["domicile", "niwas", "निवास", "mool niwas"],
    "Income Certificate": ["income", "aay", "आय", "income certificate"],
    "Caste Certificate": ["caste", "jati", "जाति", "caste certificate"],
    "Disability Certificate": ["disability", "disabled", "विकलांग", "divyang", "handicap"],
    "Student ID": ["student id", "college id", "id card", "school id", "marksheet"]
}

class ProfilerAgent:
    def __init__(self):
        self.api_key = OPENAI_API_KEY

    def extract_value(self, field: str, text: str) -> Any:
        """
        Extracts structured value for a specific field from conversational user text.
        Attempts to use LLM first if API key is present, otherwise falls back to local parsing.
        """
        if self.api_key:
            try:
                return self._extract_with_llm(field, text)
            except Exception as e:
                logger.error(f"LLM profiling failed, falling back to local: {e}")
                
        return self._extract_with_rules(field, text)

    def _extract_with_rules(self, field: str, text: str) -> Any:
        """
        Fallback rule-based extraction supporting Hindi, Hinglish, and English keywords.
        """
        clean_text = text.strip().lower()

        # 1. Full Name
        if field == "full_name":
            # For names, if the answer is long like "My name is Raj", extract "Raj"
            name_match = re.search(r"(?:my name is|mera naam|naam|naam hai)\s+([a-zA-Z\s]+)", clean_text)
            if name_match:
                return name_match.group(1).title().strip()
            return text.strip()  # Direct fallback

        # 2. Age
        elif field == "age":
            numbers = re.findall(r"\d+", clean_text)
            if numbers:
                val = int(numbers[0])
                return val if 0 < val < 120 else None
            return None

        # 3. Income
        elif field == "income":
            # Remove commas or space formatting
            text_no_comma = re.sub(r"[, ]", "", clean_text)
            # Find numbers
            numbers = re.findall(r"\d+", text_no_comma)
            if numbers:
                val = float(numbers[0])
                # Handle common words like "lakh" or "lacs" or "lakhs"
                if "lakh" in clean_text or "lac" in clean_text or "लाख" in clean_text:
                    val = val * 100000
                elif "k" in clean_text or "thousand" in clean_text or "हजार" in clean_text:
                    val = val * 1000
                return val
            return None

        # 4. Gender
        elif field == "gender":
            if "female" in clean_text or "mahila" in clean_text or "महिला" in clean_text:
                return "Female"
            if "male" in clean_text or "purush" in clean_text or "पुरुष" in clean_text:
                return "Male"
            return "Other"

        # 5. State
        elif field == "state":
            for kw, standard_state in STATE_MAP.items():
                if kw in clean_text:
                    return standard_state
            # Return capitalised text if no match found
            return text.strip().title()

        # 6. Occupation
        elif field == "occupation":
            for kw, standard_occ in OCCUPATION_MAP.items():
                if kw in clean_text:
                    return standard_occ
            return "Unemployed"  # Default fallback if not recognized

        # 7. Category
        elif field == "social_category":
            for kw, standard_cat in CATEGORY_MAP.items():
                if kw in clean_text:
                    return standard_cat
            return "General"

        # 8. Boolean Yes/No Fields (landholder, is_disabled, requires_own_house)
        elif field in ["landholder", "is_disabled", "requires_own_house", "is_student", "is_widow", "is_senior_citizen"]:
            yes_words = ["yes", "yeah", "yup", "y", "haan", "ha", "है", "हाँ", "true", "sahi", "rakhta"]
            no_words = ["no", "nah", "n", "nahi", "nahin", "na", "नहीं", "false", "galat", "ni"]
            
            for w in yes_words:
                if re.search(r"\b" + re.escape(w) + r"\b", clean_text) or w in clean_text:
                    # Specific reverse logic: requires_own_house is stored as a condition
                    # but our scheme files match "requires_own_house: false".
                    # Let's return True/False based on the word.
                    return True
            for w in no_words:
                if re.search(r"\b" + re.escape(w) + r"\b", clean_text) or w in clean_text:
                    return False
            return None

        # 9. Available Documents (Array of Strings)
        elif field == "available_documents":
            found_docs = []
            
            # Simple keyword search for all documents
            for doc_name, keywords in DOCUMENT_KEYWORDS.items():
                for kw in keywords:
                    if kw in clean_text:
                        found_docs.append(doc_name)
                        break
            
            # Fallback if they write 'all' or 'sare'
            if "all" in clean_text or "sare" in clean_text or "सभी" in clean_text:
                return list(DOCUMENT_KEYWORDS.keys())
                
            return found_docs

        return text.strip()

    def _extract_with_llm(self, field: str, text: str) -> Any:
        """
        Uses OpenAI Chat Completion API to extract structured profiles.
        """
        import openai
        client = openai.OpenAI(api_key=self.api_key)
        
        prompt = f"""
        You are an AI profile extractor. Extract the value for the field '{field}' from the following user message.
        User message: "{text}"
        
        Rules:
        - If field is 'age', return a single integer.
        - If field is 'income', return a float (convert phrases like "1.5 lakh" to 150000).
        - If field is 'gender', return "Male", "Female", or "Other".
        - If field is 'occupation', map to one of: "Student", "Farmer", "Business Owner", "Unemployed", "Salaried".
        - If field is 'social_category', map to one of: "General", "OBC", "SC", "ST", "EWS".
        - If field is boolean (e.g., landholder, is_disabled, requires_own_house), return true or false.
        - If field is 'available_documents', return a JSON list of documents from: {list(DOCUMENT_KEYWORDS.keys())}.
        - If field is 'full_name' or 'state', return the name or state capitalized.
        
        Return ONLY valid raw JSON containing a key "value" with the extracted value. No explanation, no markdown formatting.
        Example: {{"value": 23}} or {{"value": "Farmer"}} or {{"value": ["Aadhaar Card", "Bank Passbook"]}}
        """
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )
        
        res_text = response.choices[0].message.content.strip()
        data = json.loads(res_text)
        return data.get("value")
