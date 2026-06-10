from typing import List, Dict, Any

# Guidelines for obtaining documents in India
DOCUMENT_GUIDELINES = {
    "Aadhaar Card": {
        "steps": [
            "Visit the nearest Aadhaar Enrolment Centre (UIDAI).",
            "Fill out the Aadhaar Enrolment Form.",
            "Submit biometric details (fingerprints and iris scan) and identity/address proofs.",
            "Aadhaar is generated and dispatched within 10-15 days. E-Aadhaar can be downloaded online."
        ],
        "timeline": "10-15 Days",
        "official_link": "https://uidai.gov.in/"
    },
    "Ration Card": {
        "steps": [
            "Apply online through your State Food and Civil Supplies portal or visit the nearest Circle Office.",
            "Submit Application Form along with Aadhaar card copies, Income Certificate, and gas connection details.",
            "Physical verification of residence will be done by a food inspector.",
            "Ration card is issued after verification."
        ],
        "timeline": "15-30 Days",
        "official_link": "https://nfsa.gov.in/"
    },
    "Bank Passbook": {
        "steps": [
            "Visit the nearest branch of any commercial bank (SBI, PNB, etc.) or post office.",
            "Ask to open a 'Pradhan Mantri Jan Dhan Yojana' (PMJDY) zero-balance account.",
            "Submit Aadhaar Card and PAN card (or Form 60) along with 2 passport photographs.",
            "Passbook is issued instantly, and Rupay debit card will arrive by post."
        ],
        "timeline": "1-2 Days",
        "official_link": "https://pmjdy.gov.in/"
    },
    "Land Record / Land Ownership Certificate": {
        "steps": [
            "Access your State Bhulekh (Land Records) portal online.",
            "Select your District, Tehsil, and Village, then enter your Khasra or Khatauni number.",
            "Download/print the digitally signed copy of your land records.",
            "Alternatively, visit the local Tehsil office and request the Patwari or Lekhpal for an official copy."
        ],
        "timeline": "2-5 Days",
        "official_link": "https://dilrmp.gov.in/"
    },
    "Samagra ID": {
        "steps": [
            "Go to the official Samagra Portal (samagra.gov.in) (Madhya Pradesh residents only).",
            "Click on 'Register Family / Member' under the Samagra Profile section.",
            "Enter details of family members, upload Aadhaar card, and perform Aadhaar OTP e-KYC.",
            "Samagra ID will be generated and approved by the local municipal/block office."
        ],
        "timeline": "2-3 Days",
        "official_link": "https://samagra.gov.in/"
    },
    "Domicile Certificate": {
        "steps": [
            "Log in to the e-District portal of your respective State Government.",
            "Register as a new citizen and fill out the Domicile Certificate Application Form.",
            "Upload utility bills, Aadhaar card, school leaving certificate, and self-declaration form.",
            "Pay the nominal fee (usually ₹15-30) and download the signed certificate once approved."
        ],
        "timeline": "7-10 Days",
        "official_link": "https://services.india.gov.in/"
    },
    "Income Certificate": {
        "steps": [
            "Apply online via your State e-District portal or visit the local SDM/Tehsildar/CSC office.",
            "Provide proof of salary (salary slips / Form 16) or an affidavit of agricultural/business income.",
            "Submit identity and residence proof along with a self-declaration statement.",
            "The Patwari/Revenue officer will conduct verification before issuing the certificate."
        ],
        "timeline": "7-10 Days",
        "official_link": "https://services.india.gov.in/"
    },
    "Caste Certificate": {
        "steps": [
            "Apply online through the State e-District portal or the Social Welfare Office.",
            "Submit proof of caste (father's or close blood relative's caste certificate), identity proof, and affidavit.",
            "Local inquiry will be conducted by the revenue inspector.",
            "Download the digital certificate or collect it from the local block office."
        ],
        "timeline": "10-15 Days",
        "official_link": "https://services.india.gov.in/"
    },
    "Disability Certificate": {
        "steps": [
            "Register on the Unique Disability ID (UDID) portal (swavlambancard.gov.in).",
            "Fill in personal, medical, and employment details, and upload identity/address proofs.",
            "Select the nearest government hospital for medical assessment.",
            "Visit the hospital on the scheduled date for assessment by the medical board. The digital card will be dispatched after approval."
        ],
        "timeline": "15-20 Days",
        "official_link": "https://www.swavlambancard.gov.in/"
    },
    "Student ID": {
        "steps": [
            "Visit the administrative block or registrar's office of your school/college.",
            "Present your Admission Fee Receipt and passport-sized photographs.",
            "Collect your student identity card once printed and signed by the principal/dean."
        ],
        "timeline": "2-3 Days",
        "official_link": ""
    }
}

class DocumentGapAgent:
    def __init__(self):
        pass

    def analyze_documents(self, required_docs: List[str], available_docs: List[str]) -> Dict[str, Any]:
        """
        Compares required documents with available ones and returns structured analysis.
        """
        available = []
        missing = []
        
        for doc in required_docs:
            # Match documents by string containment/equality
            is_found = False
            for av_doc in available_docs:
                if doc.lower().strip() in av_doc.lower().strip() or av_doc.lower().strip() in doc.lower().strip():
                    available.append(doc)
                    is_found = True
                    break
            if not is_found:
                missing.append(doc)
                
        total_req = len(required_docs)
        readiness_score = int((len(available) / max(total_req, 1)) * 100)
        
        return {
            "required": required_docs,
            "available": available,
            "missing": missing,
            "readiness_score": readiness_score
        }


class ActionPlanAgent:
    def __init__(self):
        pass

    def generate_plan(self, missing_docs: List[str], eligible_schemes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generates step-by-step action plan to obtain missing documents and then apply for schemes.
        """
        steps = []
        total_days = 0
        
        # Step group 1: Obtaining documents
        step_idx = 1
        for doc in missing_docs:
            guide = DOCUMENT_GUIDELINES.get(doc, {
                "steps": [f"Visit the local government administrative block (Tehsil/SDM/CSC) to enquire about {doc}."],
                "timeline": "5-7 Days",
                "official_link": "https://www.india.gov.in/"
            })
            
            # Estimate days as integer from timeline string (e.g. "7-10 Days" -> 10)
            timeline_str = guide["timeline"]
            days_match = [int(s) for s in timeline_str.replace("-", " ").split() if s.isdigit()]
            days = days_match[-1] if days_match else 5
            total_days += days
            
            steps.append({
                "step_number": step_idx,
                "title": f"Obtain {doc}",
                "description": f"To apply for your eligible schemes, you first need to obtain your {doc}.",
                "actions": guide["steps"],
                "estimated_time": timeline_str,
                "official_link": guide.get("official_link"),
                "status": "pending"
            })
            step_idx += 1
            
        # Step group 2: Applying for schemes
        for scheme in eligible_schemes:
            steps.append({
                "step_number": step_idx,
                "title": f"Apply for {scheme['scheme_name']}",
                "description": f"Once all documents are ready, submit your application for the scheme.",
                "actions": scheme.get("application_steps", []),
                "estimated_time": "1-3 Days",
                "official_link": scheme.get("official_link"),
                "status": "ready_after_docs" if missing_docs else "ready"
            })
            step_idx += 1
            total_days += 2  # Average application processing step time
            
        return {
            "steps": steps,
            "estimated_completion_days": total_days,
            "summary": f"Your plan contains {len(missing_docs)} document preparation steps and {len(eligible_schemes)} scheme application steps. Total estimated readiness: {total_days} days."
        }
