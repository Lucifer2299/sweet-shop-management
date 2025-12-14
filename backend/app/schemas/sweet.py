from pydantic import BaseModel, Field


class SweetCreate(BaseModel):
    name: str
    category: str
    price: float = Field(gt=0)
    quantity: int = Field(ge=0)


class SweetResponse(SweetCreate):
    id: int

    class Config:
        from_attributes = True

