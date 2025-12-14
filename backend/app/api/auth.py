from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import UserCreateRequest, UserLoginRequest, TokenResponse
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
)

router = APIRouter()   # ⚠️ NO PREFIX HERE

@router.post("/register", status_code=201)
def register_user(data: UserCreateRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=data.email,
        hashed_password=get_password_hash(data.password),
        role="customer",
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "registered"}


@router.post("/login", response_model=TokenResponse)
@router.post("/login", response_model=TokenResponse)
@router.post("/login")
def login_user(data: UserLoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    print("USER:", user.email)
    print("HASH:", user.hashed_password)
    print("PASS:", data.password)
    return {"debug": "reached"}

