# auth.py
from datetime import datetime, timedelta
from typing import Union, Annotated
import jwt
import os
from dotenv import load_dotenv
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from starlette import status
from config.customResponse import ApiResponse
from config.database import db
from schemas.auth import UserCreate

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

users_collection = db["users"]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_user_by_username(username: str):
    return await users_collection.find_one({"username": username})

def object_id_to_str(document):
    if document is None:
        return None
    document["_id"] = str(document["_id"])
    return document

async def register_user(user: UserCreate):
    existing_user = await get_user_by_username(user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    hashed_password = hash_password(user.password)
    user_data = {
        "username": user.username,
        "email": user.email,
        "hashed_password": hashed_password,
        "role": "user"
    }
    new_user = await users_collection.insert_one(user_data)
    created_user = await users_collection.find_one({"_id": new_user.inserted_id})
    return ApiResponse(status_code=201, status="success", message="Register Successfully", data=object_id_to_str(created_user))

async def login(username: str, password: str):
    user = await get_user_by_username(username)
    if not user or not verify_password(password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user["username"]})
    # user_data = {
    #     "username": user["username"],
    #     "email": user["email"],
    #     "access_token": access_token,
    #     "token_type": "bearer"
    # }

    print(access_token)

    return {"access_token": access_token, "token_type": "bearer"}

    # return ApiResponse(status_code=200, status="success", message="Login Successfully", data=access_token)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    print("Received token:", token)

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")

        print("Payload:", payload)
        print("Username:", username)

        if username is None:
            raise credentials_exception
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.PyJWTError as e:
        print("JWT Error:", str(e))
        raise credentials_exception

    user = await get_user_by_username(username=username)
    if user is None:
        print(f"User not found: {username}")
        raise credentials_exception

    return user

def check_user_role(required_role: str):
    async def role_checker(current_user: dict = Depends(get_current_user)):
        user = current_user
        role = user.get("role")

        if role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted",
            )
        return user
    return role_checker