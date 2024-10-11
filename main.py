from fastapi import FastAPI
from auth.roleAuth import RoleMiddleware
from routers import routerProduct, routerAuth

app = FastAPI()

allowed_roles = ["admin", "user"]
app.add_middleware(RoleMiddleware, allowed_roles=allowed_roles)
app.include_router(routerProduct.router)
app.include_router(routerAuth.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Tedikap API"}
