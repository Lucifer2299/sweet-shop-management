from fastapi import APIRouter, status
from app.schemas.auth import UserRegisterRequest

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(payload: UserRegisterRequest):
    return {
        "email": payload.email,
        "message": "user registered"
    }


