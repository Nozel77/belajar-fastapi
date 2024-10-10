# app/controllers/product_controller.py
from models.product import ProductModel
from schemas.product import ProductCreate, ProductUpdate

class ProductController:
    @staticmethod
    async def get_all_products():
        return await ProductModel.get_all_products()

    @staticmethod
    async def get_product_by_id(product_id: str):
        return await ProductModel.get_product_by_id(product_id)

    @staticmethod
    async def create_product(product: ProductCreate):
        product_data = product.dict()
        return await ProductModel.create_product(product_data)

    @staticmethod
    async def update_product(product_id: str, product: ProductUpdate):
        product_data = product.dict(exclude_unset=True)
        return await ProductModel.update_product(product_id, product_data)

    @staticmethod
    async def delete_product(product_id: str):
        return await ProductModel.delete_product(product_id)
