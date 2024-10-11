from fastapi import FastAPI, Depends

from routers import routerProduct, routerAuth

app = FastAPI()
app.include_router(routerProduct.router)
app.include_router(routerAuth.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Tedikap API"}
