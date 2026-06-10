import json
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from backend.app.database import get_db
from backend.app.models import Scheme, User
from backend.app.schemas import SchemeCreate, SchemeResponse
from backend.app.auth import get_current_user
from backend.app.agents.coordinator import get_all_schemes_list, _cached_schemes

router = APIRouter(prefix="/api/schemes", tags=["schemes"])

@router.get("", response_model=List[SchemeResponse])
def list_schemes(db: Session = Depends(get_db)):
    """
    Returns all registered welfare schemes.
    """
    schemes = get_all_schemes_list(db)
    response_data = []
    for s in schemes:
        response_data.append(SchemeResponse(
            scheme_id=s["scheme_id"],
            scheme_name=s["scheme_name"],
            ministry=s["ministry"],
            state=s["state"],
            eligibility_rules=s["eligibility_rules"],
            benefits=s["benefits"],
            required_documents=s["required_documents"],
            application_steps=s["application_steps"],
            official_link=s["official_link"],
            faqs=s.get("faqs", [])
        ))
    return response_data

@router.get("/{scheme_id}", response_model=SchemeResponse)
def get_scheme(scheme_id: str, db: Session = Depends(get_db)):
    """
    Fetches details of a specific welfare scheme.
    """
    s = db.query(Scheme).filter(Scheme.id == scheme_id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Scheme not found")
        
    return SchemeResponse(
        scheme_id=s.id,
        scheme_name=s.name,
        ministry=s.ministry,
        state=s.state,
        eligibility_rules=json.loads(s.eligibility_rules),
        benefits=json.loads(s.benefits),
        required_documents=json.loads(s.required_documents),
        application_steps=json.loads(s.application_steps),
        official_link=s.official_link,
        faqs=json.loads(s.faqs)
    )

@router.post("/admin/add", response_model=SchemeResponse)
def add_scheme(scheme_in: SchemeCreate, db: Session = Depends(get_db)):
    """
    Adds a new welfare scheme to the database. (Admin Panel)
    """
    # Check if scheme already exists
    exists = db.query(Scheme).filter(Scheme.id == scheme_in.scheme_id).first()
    if exists:
        raise HTTPException(status_code=400, detail="Scheme ID already exists")
        
    db_scheme = Scheme(
        id=scheme_in.scheme_id,
        name=scheme_in.scheme_name,
        ministry=scheme_in.ministry,
        state=scheme_in.state,
        eligibility_rules=json.dumps(scheme_in.eligibility_rules.model_dump()),
        benefits=json.dumps(scheme_in.benefits),
        required_documents=json.dumps(scheme_in.required_documents),
        application_steps=json.dumps(scheme_in.application_steps),
        official_link=scheme_in.official_link,
        faqs=json.dumps([faq.model_dump() for faq in scheme_in.faqs])
    )
    
    db.add(db_scheme)
    db.commit()
    db.refresh(db_scheme)
    
    # Invalidate scheme cache
    global _cached_schemes
    _cached_schemes = []
    
    return SchemeResponse(
        scheme_id=db_scheme.id,
        scheme_name=db_scheme.name,
        ministry=db_scheme.ministry,
        state=db_scheme.state,
        eligibility_rules=json.loads(db_scheme.eligibility_rules),
        benefits=json.loads(db_scheme.benefits),
        required_documents=json.loads(db_scheme.required_documents),
        application_steps=json.loads(db_scheme.application_steps),
        official_link=db_scheme.official_link,
        faqs=json.loads(db_scheme.faqs)
    )

@router.delete("/admin/{scheme_id}")
def delete_scheme(scheme_id: str, db: Session = Depends(get_db)):
    """
    Deletes a welfare scheme from the database. (Admin Panel)
    """
    s = db.query(Scheme).filter(Scheme.id == scheme_id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Scheme not found")
        
    db.delete(s)
    db.commit()
    
    # Invalidate cache
    global _cached_schemes
    _cached_schemes = []
    
    return {"message": f"Scheme {scheme_id} deleted successfully."}

@router.post("/admin/upload-pdf")
async def upload_pdf(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Simulates uploading a government PDF guideline, extracting rules and FAQs using agentic parsing,
    and outputting a draft scheme JSON.
    """
    contents = await file.read()
    # Simple mockup PDF text parsing based on standard layout
    extracted_text = f"Parsed Guidelines for PDF: {file.filename}. Content Length: {len(contents)} bytes."
    
    # Mocking Agentic Document parsing structure
    # For a real PDF, we'd run PyPDF2 / pdfplumber and feed text to OpenAI to structure rules.
    # We return a structured mock draft scheme that the administrator can review and edit in the dashboard.
    draft_scheme = {
        "scheme_id": f"draft_{file.filename.split('.')[0].lower()}",
        "scheme_name": f"New Policy Scheme ({file.filename.split('.')[0].replace('_', ' ').title()})",
        "ministry": "Ministry of Welfare & Citizen Empowerment",
        "state": "Central",
        "eligibility_rules": {
            "occupations": ["Unemployed", "Student"],
            "max_income": 300000.0,
            "min_age": 18,
            "max_age": 35,
            "genders": ["Male", "Female"],
            "states": [],
            "social_categories": [],
            "is_student": True
        },
        "benefits": [
            "Financial stipend of Rs. 2,000 per month.",
            "Free access to skills development modules."
        ],
        "required_documents": [
            "Aadhaar Card",
            "Student ID",
            "Income Certificate"
        ],
        "application_steps": [
            "Visit the welfare dashboard online.",
            "Upload verified student credential certificates.",
            "Wait for bank account linking validation."
        ],
        "official_link": "https://welfare.gov.in/",
        "faqs": [
            {
                "question": "Is this draft verified?",
                "answer": "This is a draft parsed from uploaded PDF files. Please verify all details before submitting."
            }
        ]
    }
    
    return {
        "filename": file.filename,
        "message": "PDF guideline parsed successfully by Document Agent.",
        "draft_scheme": draft_scheme
    }
