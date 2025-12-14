from pydantic import BaseModel, EmailStr, Field


# -------------------------
# Requests
# -------------------------

class UserCreateRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


# -------------------------
# Responses
# -------------------------

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    email: EmailStr
    role: str

    class Config:
        from_attributes = True

from pydantic import BaseModel, Field
from typing import Literal


class UserRoleUpdate(BaseModel):
    role: Literal["admin", "staff", "customer"] = Field(
        ...,
        description="New role for the user",
        examples=["staff"],
    )

