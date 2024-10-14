from pydantic import BaseModel
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    regular_price: int
    large_price: int
    category: str
    image: Optional[str] = None

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    regular_price: Optional[int] = None
    large_price: Optional[int] = None
    category: Optional[str] = None
    image: Optional[str] = None

class ProductResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    regular_price: int
    large_price: int
    category: str
    image: str

    class Config:
        from_attributes = True


