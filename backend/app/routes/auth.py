from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models import User
from backend.app.schemas import UserRegister, Token
from backend.app.auth import create_access_token

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register", response_model=Token)
def register_or_login(user_in: UserRegister, db: Session = Depends(get_db)):
    """
    Registers a new user using their phone number, or logs them in if they already exist.
    Generates a secure JWT access token.
    """
    # Simple validation for 10 digit Indian phone numbers
    phone = user_in.phone.strip()
    if not phone.isdigit() or len(phone) < 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid phone number. Must be at least 10 digits."
        )
        
    db_user = db.query(User).filter(User.phone == phone).first()
    if not db_user:
        db_user = User(
            phone=phone,
            full_name=user_in.full_name or "Citizen",
            preferred_language=user_in.preferred_language
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    else:
        # If user exists, optionally update language if sent
        if user_in.preferred_language:
            db_user.preferred_language = user_in.preferred_language
            db.commit()
            db.refresh(db_user)

    # Create access token
    access_token = create_access_token(data={"sub": db_user.phone})
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user_id=db_user.id,
        full_name=db_user.full_name,
        preferred_language=db_user.preferred_language
    )
