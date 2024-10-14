from fastapi import FastAPI

from routers import routerProduct, routerAuth, routerUser

app = FastAPI()
app.include_router(routerProduct.router)
app.include_router(routerAuth.router)
app.include_router(routerUser.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Tedikap API"}
