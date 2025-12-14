from typing import List, Optional

from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_role
from app.db.session import get_db
from app.models.sweet import Sweet
from app.schemas.sweet import SweetCreate, SweetResponse
from app.models.user import User

router = APIRouter(tags=["Sweets"])


# -------------------------
# CREATE SWEET (ADMIN)
# -------------------------
@router.post(
    "",
    response_model=SweetResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_sweet(
    data: SweetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    sweet = Sweet(**data.model_dump())
    db.add(sweet)
    db.commit()
    db.refresh(sweet)
    return sweet


# -------------------------
# LIST SWEETS
# -------------------------
@router.get(
    "",
    response_model=List[SweetResponse],
)
def list_sweets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(Sweet).all()


# -------------------------
# SEARCH SWEETS
# -------------------------
@router.get(
    "/search",
    response_model=List[SweetResponse],
)
def search_sweets(
    name: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Sweet)

    if name:
        query = query.filter(Sweet.name.ilike(f"%{name}%"))

    if category:
        query = query.filter(Sweet.category == category)

    if min_price is not None:
        query = query.filter(Sweet.price >= min_price)

    if max_price is not None:
        query = query.filter(Sweet.price <= max_price)

    return query.all()

