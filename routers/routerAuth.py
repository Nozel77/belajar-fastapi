from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from config.customResponse import ApiResponse
from controllers.controllerAuth import register_user, login
from schemas.auth import UserCreate

router = APIRouter()

@router.post("/register", response_model=ApiResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate):
    registered_user = await register_user(user)
    return registered_user

@router.post("/login", status_code=status.HTTP_200_OK)
async def login_endpoint(form_data: OAuth2PasswordRequestForm = Depends()):
    return await login(form_data.username, form_data.password)

