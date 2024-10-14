from fastapi import APIRouter, HTTPException, status, Depends

from config.customResponse import ApiResponse
from controllers.controllerAuth import get_current_user, check_user_role
from schemas.product import ProductCreate, ProductUpdate
from controllers.controllerProduct import ProductController
from schemas.validators import validate_object_id

router = APIRouter(
    prefix="/product",
    tags=["product"],
)

@router.get("/", response_model=ApiResponse)
async def get_all_products(user: dict = Depends(get_current_user)):
    print(user)
    products = await ProductController.get_all_products()
    return ApiResponse(status_code=200, status="success", message="Success getting all data", data=products)

@router.get("/{id}", response_model=ApiResponse)
async def get_product(id: str, user: dict = Depends(get_current_user)):
    validate_object_id(id)
    product = await ProductController.get_product_by_id(id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return ApiResponse(status_code=200, status="success", message="Success getting data", data=product)

@router.post("/", response_model=ApiResponse, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate,user: dict = Depends(check_user_role("admin"))):
    created_product = await ProductController.create_product(product)
    return ApiResponse(status_code=201, status="success", message="Success creating data", data=created_product)

@router.put("/{id}", response_model=ApiResponse, status_code=status.HTTP_200_OK)
async def update_product(id: str, product: ProductUpdate, user: dict = Depends(check_user_role("admin"))):
    validate_object_id(id)
    updated_product = await ProductController.update_product(id, product)
    if updated_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return ApiResponse(status_code=200, status="success", message="Success updating data", data=updated_product)

@router.delete("/{id}", response_model=ApiResponse, status_code=status.HTTP_200_OK)
async def delete_product(id: str, user: dict = Depends(check_user_role("admin"))):
    validate_object_id(id)
    deleted_count = await ProductController.delete_product(id)
    if deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return ApiResponse(status_code=200, status="success", message="Success deleting data", data=None)
