from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
app = FastAPI()

class Product(BaseModel):
    id: Optional[int] = None
    name: str
    description: str
    regular_price: int
    large_price: int
    category: str
    image: str

class ProductCreate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    regular_price: Optional[int] = None
    large_price: Optional[int] = None
    category: Optional[str] = None
    image: Optional[str] = None

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    regular_price: Optional[int] = None
    large_price: Optional[int] = None
    category: Optional[str] = None
    image: Optional[str] = None


PRODUCT = [
    {
        "id": 1,
        "name": "Mango Tea",
        "description": "Teh mangga manis.",
        "regular_price": 5000,
        "large_price": 8000,
        "category": "tea",
        "image": "mangotea.jpg",
    },
    {
        "id": 2,
        "name": "Lemonade",
        "description": "Air lemon yang menyegarkan",
        "regular_price": 5000,
        "large_price": 8000,
        "category": "nontea",
        "image": "lemonade.jpg",
    },
    {
        "id": 3,
        "name": "Choco Hazelnut",
        "description": "Choco Hazelnut yang lezat.",
        "regular_price": 5000,
        "large_price": 7000,
        "category": "nontea",
        "image": "hazelnut.jpg",
    },
    {
        "id": 4,
        "name": "Original Tea",
        "description": "Original Tea Lezat.",
        "regular_price": 3000,
        "large_price": 0,
        "category": "tea",
        "image": "original.jpg",
    },
    {
        "id": 5,
        "name": "Yakult Orange",
        "description": "Delicious Yakult Series.",
        "regular_price": 8500,
        "large_price": 12000,
        "category": "yakult",
        "image": "yakultorange.jpeg",
    },
    {
        "id": 6,
        "name": "Yakult Strawberry",
        "description": "Delicious Yakult Series.",
        "regular_price": 8500,
        "large_price": 12000,
        "category": "yakult",
        "image": "yakultstrawberry.jpg",
    },
    {
        "id": 7,
        "name": "Peach Tea",
        "description": "Teh rasa peach yang segar.",
        "regular_price": 6000,
        "large_price": 8000,
        "category": "tea",
        "image": "peachtea.jpeg",
    },
    {
        "id": 8,
        "name": "Green Tea Latte",
        "description": "Latte dengan rasa teh hijau.",
        "regular_price": 7000,
        "large_price": 9000,
        "category": "tea",
        "image": "greentealatte.jpg",
    },
    {
        "id": 9,
        "name": "Ginger Tea",
        "description": "Teh madu yang harum.",
        "regular_price": 5500,
        "large_price": 7500,
        "category": "tea",
        "image": "gingertea.jpeg",
    },
    {
        "id": 10,
        "name": "Mango Smoothie",
        "description": "Smoothie mangga yang lezat.",
        "regular_price": 7000,
        "large_price": 10000,
        "category": "nontea",
        "image": "mangosmoothie.jpeg",
    },
    {
        "id": 11,
        "name": "Matcha Latte",
        "description": "Matcha latte yang nikmat.",
        "regular_price": 8000,
        "large_price": 11000,
        "category": "nontea",
        "image": "matchalatte.jpg",
    },
    {
        "id": 12,
        "name": "Banana Shake",
        "description": "Shake pisang dengan susu.",
        "regular_price": 6000,
        "large_price": 9000,
        "category": "nontea",
        "image": "bananashake.jpeg",
    },
    {
        "id": 13,
        "name": "Yakult Blueberry",
        "description": "Delicious Yakult Series.",
        "regular_price": 8500,
        "large_price": 12000,
        "category": "yakult",
        "image": "yakultblueberry.jpeg",
    },
    {
        "id": 14,
        "name": "Yakult Mango",
        "description": "Delicious Yakult Series.",
        "regular_price": 8500,
        "large_price": 12000,
        "category": "yakult",
        "image": "yakultmango.jpg",
    },
    {
        "id": 15,
        "name": "Original Tea",
        "description": "teh original dari tenka",
        "regular_price": 3000,
        "large_price": 5000,
        "category": "tea",
        "image": "1725768957.jpg",
    },
]

@app.get("/product")
async def get_all_product():
    return JSONResponse(content={"status_code": 200, "message": "Success", "data": PRODUCT})

@app.get("/product/")
async def category_filter(category: str):
    product_to_return = []
    for product in PRODUCT:
        if product.get('category').casefold() == category.casefold():
            product_to_return.append(product)
    return product_to_return

@app.get("/product/{id}")
async def get_detail_product(id: int):
    for product in PRODUCT:
        if product.get('id') == id:
            return JSONResponse(content={"status_code": 200, "message": "Success", "data": product})
    raise HTTPException(status_code=404, detail="Product not found")


@app.post("/product")
async def create_product(new_product: ProductCreate):
    if new_product.regular_price <= 0 or new_product.large_price <= 0:
        raise HTTPException(status_code=400, detail="regular price and large price must be greater than 0.")
    if len(PRODUCT) > 0:
        new_id = max([product['id'] for product in PRODUCT]) + 1
    else:
        new_id = 1
    new_product.id = new_id
    PRODUCT.append(new_product.model_dump())
    return JSONResponse(content={"status_code": 201, "message": "Product created", "data": new_product.model_dump()})

@app.put("/product/{id}")
async def update_product(id: int, updated_product: ProductUpdate):
    for product in PRODUCT:
        if product.get('id') == id:
            updated_product_dict = updated_product.model_dump()
            updated_product_dict.pop('id', None)
            product.update(updated_product_dict)
            return JSONResponse(content={"status_code": 200, "message": "Product updated", "data": product})
    raise HTTPException(status_code=404, detail="Product not found")


@app.delete("/product/{id}")
async def delete_product(id: int):
    for product in PRODUCT:
        if product.get('id') == id:
            PRODUCT.remove(product)
            return JSONResponse(content={"status_code": 200, "message": "Product deleted", "data": product})
    raise HTTPException(status_code=404, detail="Product not found")