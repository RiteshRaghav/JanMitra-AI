from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

# Auth Schemas
class UserRegister(BaseModel):
    phone: str = Field(..., description="10-digit mobile number")
    full_name: Optional[str] = None
    preferred_language: str = "English"

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: str
    full_name: Optional[str]
    preferred_language: str

class TokenData(BaseModel):
    phone: Optional[str] = None

class UserResponse(BaseModel):
    id: str
    phone: str
    full_name: Optional[str]
    preferred_language: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# Chat Schemas
class MessageResponse(BaseModel):
    id: str
    sender: str
    text: str
    voice_url: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class StartChatRequest(BaseModel):
    preferred_language: Optional[str] = None

class StartChatResponse(BaseModel):
    conversation_id: str
    status: str
    message: str
    next_question: str
    question_count: int
    is_completed: bool

class MessageRequest(BaseModel):
    conversation_id: str
    text: str

class MessageAnswerResponse(BaseModel):
    message: MessageResponse
    next_question: Optional[str] = None
    question_count: int
    is_completed: bool
    results: Optional[Dict[str, Any]] = None

# Scheme Schemas
class SchemeFAQ(BaseModel):
    question: str
    answer: str

class SchemeRules(BaseModel):
    occupations: List[str] = []
    max_income: Optional[float] = None
    landholder: Optional[bool] = None
    min_age: Optional[int] = 0
    max_age: Optional[int] = 120
    genders: List[str] = []
    states: List[str] = []
    social_categories: List[str] = []
    is_student: Optional[bool] = None
    is_disabled: Optional[bool] = None
    is_widow: Optional[bool] = None
    is_senior_citizen: Optional[bool] = None
    requires_own_house: Optional[bool] = None

class SchemeCreate(BaseModel):
    scheme_id: str
    scheme_name: str
    ministry: str
    state: str
    eligibility_rules: SchemeRules
    benefits: List[str]
    required_documents: List[str]
    application_steps: List[str]
    official_link: str
    faqs: List[SchemeFAQ] = []

class SchemeResponse(BaseModel):
    scheme_id: str
    scheme_name: str
    ministry: str
    state: str
    eligibility_rules: Dict[str, Any]
    benefits: List[str]
    required_documents: List[str]
    application_steps: List[str]
    official_link: str
    faqs: List[Dict[str, str]]

    class Config:
        from_attributes = True

# Document Schemas
class DocumentToggleRequest(BaseModel):
    document_name: str
    is_available: bool

class UserDocumentResponse(BaseModel):
    document_name: str
    is_available: bool

    class Config:
        from_attributes = True
