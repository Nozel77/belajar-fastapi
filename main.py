from fastapi import FastAPI
from routers import routerProduct

app = FastAPI()

app.include_router(routerProduct.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the product API"}
