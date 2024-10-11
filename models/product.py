# app/models/product.py
from config.database import db
from bson import ObjectId

def product_helper(product) -> dict:
    return {
        "id": str(product["_id"]),
        "name": product["name"],
        "description": product["description"],
        "regular_price": product["regular_price"],
        "large_price": product["large_price"],
        "category": product["category"],
        "image": product["image"]
    }

product_collection = db["products"]

class ProductModel:
    @staticmethod
    async def get_all_products():
        products = []
        async for product in product_collection.find():
            products.append(product_helper(product))
        return products

    @staticmethod
    async def get_product_by_id(product_id: str):
        product = await product_collection.find_one({"_id": ObjectId(product_id)})
        if product:
            return product_helper(product)
        return None

    @staticmethod
    async def create_product(product_data: dict):
        new_product = await product_collection.insert_one(product_data)
        created_product = await product_collection.find_one({"_id": new_product.inserted_id})
        return product_helper(created_product)

    @staticmethod
    async def update_product(product_id: str, product_data: dict):
        updated_product = await product_collection.update_one(
            {"_id": ObjectId(product_id)}, {"$set": product_data}
        )
        if updated_product.modified_count:
            return await ProductModel.get_product_by_id(product_id)
        return None

    @staticmethod
    async def delete_product(product_id: str):
        deleted_product = await product_collection.delete_one({"_id": ObjectId(product_id)})
        return deleted_product.deleted_count
