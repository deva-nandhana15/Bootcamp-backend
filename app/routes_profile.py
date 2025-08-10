from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from .auth import get_current_user
from .database import users_col, sections_col, tasks_col

router = APIRouter(prefix="/profile", tags=["profile"])

@router.get("/")
async def get_profile(current_user: dict = Depends(get_current_user)):
    """
    Returns:
    {
      name, email,
      totalSections,
      totalTasks,
      sections: [ { name, pending, completed } ... ]
    }
    """
    uid = ObjectId(current_user["_id"])

    # total sections
    total_sections = await sections_col.count_documents({"user_id": uid})

    # total tasks
    total_tasks = await tasks_col.count_documents({"user_id": uid})

    # sections breakdown
    sections_cursor = sections_col.find({"user_id": uid})
    sections = []
    async for sec in sections_cursor:
        sec_id = sec["_id"]
        name = sec.get("name", "Unnamed")
        pending = await tasks_col.count_documents({"user_id": uid, "section_id": sec_id, "status": "pending"})
        completed = await tasks_col.count_documents({"user_id": uid, "section_id": sec_id, "status": "completed"})
        sections.append({"name": name, "pending": pending, "completed": completed})

    return {
        "name": current_user.get("name"),
        "email": current_user.get("email"),
        "totalSections": total_sections,
        "totalTasks": total_tasks,
        "sections": sections
    }
