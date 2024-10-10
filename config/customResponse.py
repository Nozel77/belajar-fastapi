from typing import Optional, Any
from pydantic import BaseModel

class ApiResponse(BaseModel):
    status_code: int
    status: str
    message: str
    data: Optional[Any]


    class Config:
        orm_mode = True
