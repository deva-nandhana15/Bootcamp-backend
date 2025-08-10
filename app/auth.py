from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from bson import ObjectId
from typing import Optional
from .database import users_col
from .utils import hash_password, verify_password, create_access_token, decode_token
from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.post("/signup", status_code=201)
async def signup(payload: dict):
    """
    payload: { name, email, password }
    """
    email = payload.get("email")
    name = payload.get("name")
    password = payload.get("password")
    if not email or not password or not name:
        raise HTTPException(status_code=400, detail="name, email, password required")
    existing = await users_col.find_one({"email": email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = hash_password(password)
    res = await users_col.insert_one({"name": name, "email": email, "password_hash": hashed})
    return {"id": str(res.inserted_id), "name": name, "email": email}

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    uses OAuth2PasswordRequestForm so frontend should send form data:
    username = email, password = password
    """
    user = await users_col.find_one({"email": form_data.username})
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    if not verify_password(form_data.password, user["password_hash"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    token = create_access_token({"user_id": str(user["_id"])})
    return {"access_token": token, "token_type": "bearer"}

# dependency
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_token(token)
        user_id: Optional[str] = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid auth token")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid auth token")
    user = await users_col.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # normalize user
    user["id"] = str(user["_id"])
    return user
