from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from app import utils  # not used here but available
from .auth import get_current_user
from .database import sections_col
from .models import SectionCreate

router = APIRouter(prefix="/sections", tags=["sections"])

@router.post("/")
async def create_section(payload: SectionCreate, current_user: dict = Depends(get_current_user)):
    user_id = ObjectId(current_user["_id"])
    res = await sections_col.insert_one({"user_id": user_id, "name": payload.name})
    return {"id": str(res.inserted_id), "name": payload.name}

@router.get("/")
async def get_sections(current_user: dict = Depends(get_current_user)):
    user_id = ObjectId(current_user["_id"])
    cursor = sections_col.find({"user_id": user_id})
    out = []
    async for sec in cursor:
        out.append({"id": str(sec["_id"]), "name": sec.get("name")})
    return out
