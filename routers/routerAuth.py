from fastapi import APIRouter, Depends, Form, status
from config.customResponse import ApiResponse
from controllers.controllerAuth import register_user, login
from schemas.auth import UserCreate, UserMe, UserLogin

router = APIRouter()

@router.post("/register", response_model=ApiResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate):
    registered_user = await register_user(user)
    return registered_user

@router.post("/login", response_model=ApiResponse, status_code=status.HTTP_200_OK)
async def login_endpoint(login_request: UserLogin):
    return await login(login_request.email, login_request.password)

# @router.get("/users/me", response_model=UserMe)
# async def read_users_me(current_user: User = Depends(get_current_user)):
#     """
#     Retrieve the current user.
#     """
#     return current_user