from bson import ObjectId
from .database import users_col, sections_col, tasks_col

# Users
async def create_user(name: str, email: str, password_hash: str):
    return await users_col.insert_one({"name": name, "email": email, "password_hash": password_hash})

# Sections
async def create_section(user_id: ObjectId, name: str):
    return await sections_col.insert_one({"user_id": user_id, "name": name})

async def list_sections_for_user(user_id: ObjectId):
    cursor = sections_col.find({"user_id": user_id})
    return [s async for s in cursor]

# Tasks
async def create_task(user_id: ObjectId, title: str, status: str = "pending", section_id = None):
    doc = {"user_id": user_id, "title": title, "status": status, "section_id": section_id}
    return await tasks_col.insert_one(doc)
