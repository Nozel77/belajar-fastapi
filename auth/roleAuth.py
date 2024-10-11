import os
from dotenv import load_dotenv
from fastapi import Request, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from starlette.middleware.base import BaseHTTPMiddleware
import jwt
from config.database import db
from controllers.controllerAuth import get_current_user

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

users_collection = db["users"]

class RoleMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, allowed_roles: list):
        super().__init__(app)
        self.allowed_roles = allowed_roles

    async def dispatch(self, request: Request, call_next):
        if request.url.path in ["/register", "/login", "/docs", "/redoc", "/openapi.json"]:
            response = await call_next(request)
            return response

        token = request.headers.get("Authorization")

        if token is None or not token.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing or invalid Authorization header",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Ambil token dari header
        token = token[len("Bearer "):]

        try:
            # Dekode token untuk mendapatkan payload
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email = payload.get("sub")
            if email is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            # Ambil user dari database
            user = await users_collection.find_one({"email": email})
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            # Cek peran pengguna
            user_role = user.get("role")
            if user_role not in self.allowed_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied: Insufficient role",
                )

        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.PyJWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        response = await call_next(request)
        return response

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def role_required(roles: list):
    current_user = await get_current_user()
    if current_user['role'] not in roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted for this role"
        )
    return current_user


