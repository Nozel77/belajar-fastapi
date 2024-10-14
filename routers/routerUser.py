from fastapi import APIRouter
from fastapi.params import Depends

from config.customResponse import ApiResponse
from controllers.controllerAuth import check_user_role
from controllers.controllerUser import UserController
from schemas.user import CreateUser, UpdateUser

router = APIRouter(
    prefix="/user",
    tags=["manage user"],
)

@router.get("/", response_model=ApiResponse)
async def get_all_user(user: dict = Depends(check_user_role("admin"))):
    user = await UserController.get_all_users()
    return ApiResponse(status_code=200, status="success", message="Success getting all data", data=user)

@router.get("/{id}", response_model=ApiResponse)
async def get_user(id: str, user: dict = Depends(check_user_role("admin"))):
    user = await UserController.get_user_by_id(id)
    if user is None:
        return ApiResponse(status_code=404, status="failed", message="User not found", data=None)
    return ApiResponse(status_code=200, status="success", message="Success getting data", data=user)

@router.post("/", response_model=ApiResponse)
async def create_user(create: CreateUser,user: dict = Depends(check_user_role("admin"))):
    created_user = await UserController.create_user(create)
    return ApiResponse(status_code=201, status="success", message="Success creating data", data=created_user)

@router.put("/{id}", response_model=ApiResponse)
async def update_user(id: str, update: UpdateUser ,user: dict = Depends(check_user_role("admin"))):
    updated_user = await UserController.update_user(id, update)
    if updated_user is None:
        return ApiResponse(status_code=404, status="failed", message="User not found", data=None)
    return ApiResponse(status_code=200, status="success", message="Success updating data", data=updated_user)

@router.delete("/{id}", response_model=ApiResponse)
async def delete_user(id: str, user: dict = Depends(check_user_role("admin"))):
    deleted_count = await UserController.delete_user(id)
    if deleted_count == 0:
        return ApiResponse(status_code=404, status="failed", message="User not found", data=None)
    return ApiResponse(status_code=200, status="success", message="Success deleting data", data=None)