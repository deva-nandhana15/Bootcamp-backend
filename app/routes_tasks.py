from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from .auth import get_current_user
from .database import tasks_col, sections_col
from .models import TaskCreate

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/")
async def create_task(payload: TaskCreate, current_user: dict = Depends(get_current_user)):
    user_id = ObjectId(current_user["_id"])
    section_oid = None
    if payload.section_id:
        try:
            section_oid = ObjectId(payload.section_id)
            # optionally verify section belongs to user
            sec = await sections_col.find_one({"_id": section_oid, "user_id": user_id})
            if not sec:
                raise HTTPException(status_code=400, detail="Section not found for user")
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid section_id")
    doc = {"user_id": user_id, "title": payload.title, "status": payload.status, "section_id": section_oid}
    res = await tasks_col.insert_one(doc)
    return {"id": str(res.inserted_id), "title": payload.title, "status": payload.status, "section_id": payload.section_id}

@router.get("/")
async def list_tasks(current_user: dict = Depends(get_current_user)):
    user_id = ObjectId(current_user["_id"])
    cursor = tasks_col.find({"user_id": user_id})
    out = []
    async for t in cursor:
        out.append({
            "id": str(t["_id"]),
            "title": t.get("title"),
            "status": t.get("status"),
            "section_id": str(t["section_id"]) if t.get("section_id") else None
        })
    return out

@router.patch("/{task_id}")
async def update_task(task_id: str, payload: dict, current_user: dict = Depends(get_current_user)):
    user_id = ObjectId(current_user["_id"])
    try:
        tid = ObjectId(task_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid task id")
    update = {}
    if "title" in payload:
        update["title"] = payload["title"]
    if "status" in payload:
        update["status"] = payload["status"]
    if "section_id" in payload:
        update["section_id"] = ObjectId(payload["section_id"]) if payload["section_id"] else None
    if not update:
        raise HTTPException(status_code=400, detail="No fields to update")
    result = await tasks_col.update_one({"_id": tid, "user_id": user_id}, {"$set": update})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "updated"}
