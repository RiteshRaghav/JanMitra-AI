from typing import Dict, Any, List, Optional

QUESTIONS = [
    {
        "field": "full_name",
        "depends_on": None,
        "prompts": {
            "English": "Welcome! What is your full name?",
            "Hindi": "स्वागत है! आपका पूरा नाम क्या है?",
            "Hinglish": "Welcome! Aapka full name kya hai?"
        }
    },
    {
        "field": "age",
        "depends_on": None,
        "prompts": {
            "English": "What is your age?",
            "Hindi": "आपकी उम्र क्या है?",
            "Hinglish": "Aapki age kya hai?"
        }
    },
    {
        "field": "gender",
        "depends_on": None,
        "prompts": {
            "English": "What is your gender? (Male/Female/Other)",
            "Hindi": "आपका लिंग क्या है? (पुरुष/महिला/अन्य)",
            "Hinglish": "Aapka gender kya hai? (Male/Female/Other)"
        }
    },
    {
        "field": "state",
        "depends_on": None,
        "prompts": {
            "English": "Which state do you live in? (e.g. Madhya Pradesh, Uttar Pradesh, Haryana, Delhi, etc.)",
            "Hindi": "आप किस राज्य में रहते हैं? (जैसे: मध्य प्रदेश, उत्तर प्रदेश, हरियाणा, दिल्ली)",
            "Hinglish": "Aap kis state me rehte hain? (e.g. Madhya Pradesh, Uttar Pradesh, Haryana, Delhi)"
        }
    },
    {
        "field": "occupation",
        "depends_on": None,
        "prompts": {
            "English": "What is your occupation? (Student / Farmer / Business Owner / Unemployed / Salaried)",
            "Hindi": "आपका मुख्य व्यवसाय क्या है? (छात्र / किसान / व्यवसायी / बेरोजगार / नौकरीपेशा)",
            "Hinglish": "Aapka occupation kya hai? (Student / Farmer / Business Owner / Unemployed / Salaried)"
        }
    },
    {
        "field": "income",
        "depends_on": None,
        "prompts": {
            "English": "What is your annual family income (in Rupees)?",
            "Hindi": "आपकी वार्षिक पारिवारिक आय कितनी है (रुपये में)?",
            "Hinglish": "Aapki annual family income kitni hai (Rs me)?"
        }
    },
    {
        "field": "social_category",
        "depends_on": None,
        "prompts": {
            "English": "What is your social category? (General / OBC / SC / ST / EWS)",
            "Hindi": "आपकी सामाजिक श्रेणी क्या है? (General / OBC / SC / ST / EWS)",
            "Hinglish": "Aapki social category kya hai? (General / OBC / SC / ST / EWS)"
        }
    },
    {
        "field": "landholder",
        "depends_on": "occupation",
        "condition": lambda p: p.get("occupation") == "Farmer",
        "prompts": {
            "English": "Do you own agricultural land? (Yes / No)",
            "Hindi": "क्या आपके पास स्वयं की कृषि भूमि है? (हाँ / नहीं)",
            "Hinglish": "Kya aapke paas kheti ki zameen hai? (Yes / No)"
        }
    },
    {
        "field": "is_disabled",
        "depends_on": None,
        "prompts": {
            "English": "Do you have any physical disability? (Yes / No)",
            "Hindi": "क्या आपको कोई शारीरिक विकलांगता है? (हाँ / नहीं)",
            "Hinglish": "Kya aapko koi physical disability hai? (Yes / No)"
        }
    },
    {
        "field": "marital_status",
        "depends_on": None,
        "prompts": {
            "English": "What is your marital status? (Single / Married / Widow / Divorced)",
            "Hindi": "आपकी वैवाहिक स्थिति क्या है? (अविवाहित / विवाहित / विधवा / तलाकशुदा)",
            "Hinglish": "Aapki marital status kya hai? (Single / Married / Widow / Divorced)"
        }
    },
    {
        "field": "requires_own_house",
        "depends_on": None,
        "prompts": {
            "English": "Do you or your family own a pucca (concrete) house in India? (Yes / No)",
            "Hindi": "क्या आपके या आपके परिवार के पास भारत में अपना पक्का घर है? (हाँ / नहीं)",
            "Hinglish": "Kya aapke paas apna pucca (concrete) ghar hai? (Yes / No)"
        }
    },
    {
        "field": "available_documents",
        "depends_on": None,
        "prompts": {
            "English": "Which documents do you currently have? (e.g. Aadhaar, Ration Card, Bank Passbook, Land Record, SAMAGRA ID, Domicile, Income/Caste Certificate)",
            "Hindi": "आपके पास इस समय कौन से दस्तावेज उपलब्ध हैं? (जैसे: आधार कार्ड, राशन कार्ड, बैंक पासबुक, जमीन के कागजात, समग्र आईडी, मूल निवासी, आय/जाति प्रमाण पत्र)",
            "Hinglish": "Aapke paas abhi kaun-kaun se documents hain? (e.g. Aadhaar, Ration Card, Bank Passbook, Land Record, SAMAGRA ID, Domicile, Income/Caste Certificate)"
        }
    }
]

class InterviewAgent:
    def __init__(self, language: str = "English"):
        self.language = language if language in ["English", "Hindi", "Hinglish"] else "English"

    def get_next_question(self, profile: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Determines the next question to ask based on the current profile keys filled.
        Intelligently skips questions that don't meet their conditions.
        """
        for q in QUESTIONS:
            field = q["field"]
            if field in profile and profile[field] is not None:
                # Question already answered
                continue
            
            # Check conditional dependency
            if q["depends_on"]:
                condition = q.get("condition")
                if condition and not condition(profile):
                    # Skip this question since condition is not met
                    continue
            
            # Additional custom skipping rules:
            # 1. Skip landholder if we already know occupation is not Farmer
            if field == "landholder" and profile.get("occupation") and profile.get("occupation") != "Farmer":
                continue
            
            # 2. Skip student conditions if not student
            if field == "education_level" and profile.get("occupation") and profile.get("occupation") != "Student":
                continue

            # Return the question with prompt in the correct language
            return {
                "field": field,
                "text": q["prompts"].get(self.language, q["prompts"]["English"])
            }
        
        return None  # All questions answered or skipped
