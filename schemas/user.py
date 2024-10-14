from enum import Enum
from typing import Optional

from pydantic import BaseModel

class UserRole(str, Enum):
    user = "user"
    admin = "admin",


class CreateUser(BaseModel):
    username: str
    password: str
    email: str
    role: UserRole

class UpdateUser(CreateUser):
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None
    role: Optional[UserRole] = None

