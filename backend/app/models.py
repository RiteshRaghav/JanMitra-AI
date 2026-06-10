import uuid
import datetime
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from backend.app.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    phone = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    preferred_language = Column(String, default="English")  # "English", "Hindi", "Hinglish"
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")
    documents = relationship("UserDocument", back_populates="user", cascade="all, delete-orphan")


class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    status = Column(String, default="active")  # "active", "completed"
    current_profile = Column(Text, default="{}")  # Stored as JSON string
    question_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")


class Message(Base):
    __tablename__ = "messages"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    conversation_id = Column(String, ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False)
    sender = Column(String, nullable=False)  # "user" or "assistant"
    text = Column(Text, nullable=False)
    voice_url = Column(String, nullable=True)  # Path/URL to TTS audio
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    conversation = relationship("Conversation", back_populates="messages")


class Scheme(Base):
    __tablename__ = "schemes"
    
    id = Column(String, primary_key=True)  # e.g., "pm_kisan"
    name = Column(String, nullable=False)
    ministry = Column(String, nullable=False)
    state = Column(String, nullable=False)  # "Central" or specific state like "Madhya Pradesh"
    eligibility_rules = Column(Text, default="{}")  # Stored as JSON string
    benefits = Column(Text, default="[]")  # Stored as JSON string
    required_documents = Column(Text, default="[]")  # Stored as JSON string
    application_steps = Column(Text, default="[]")  # Stored as JSON string
    official_link = Column(String, nullable=True)
    faqs = Column(Text, default="[]")  # Stored as JSON string
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class UserDocument(Base):
    __tablename__ = "user_documents"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    document_name = Column(String, nullable=False)  # e.g., "Aadhaar Card", "Ration Card"
    is_available = Column(Boolean, default=False)
    verified_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    user = relationship("User", back_populates="documents")


class Report(Base):
    __tablename__ = "reports"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    conversation_id = Column(String, ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False)
    pdf_path = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
