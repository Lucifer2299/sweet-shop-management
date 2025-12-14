from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import UserResponse, UserRoleUpdate
from app.api.deps import get_current_user, require_role

router = APIRouter(prefix="/api/users", tags=["Users"])


# ----------------------------
# Get current user (AUTH TEST)
# ----------------------------
@router.get("/me", response_model=UserResponse)
def read_current_user(
    current_user: User = Depends(get_current_user),
):
    return current_user


# ----------------------------
# Admin: list all users
# ----------------------------
@router.get(
    "",
    response_model=list[UserResponse],
)
def list_users(
    db: Session = Depends(get_db),
    _: User = Depends(require_role("admin")),
):
    return db.query(User).all()


# ----------------------------
# Admin: change user role
# ----------------------------
@router.patch(
    "/{email}/role",
    response_model=UserResponse,
)
def update_user_role(
    email: str,
    data: UserRoleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Prevent admin from changing their own role
    if user.email == current_user.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admin cannot change own role",
        )

    user.role = data.role
    db.commit()
    db.refresh(user)
    return user

