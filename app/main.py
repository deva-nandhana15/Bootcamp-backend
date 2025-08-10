from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from bson import ObjectId
from .database import users_col, sections_col, tasks_col
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # change to frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# MODELS
# -----------------------------
class TaskModel(BaseModel):
    text: str
    completed: bool = False
    section: Optional[str] = None

class SectionModel(BaseModel):
    name: str

# -----------------------------
# ROUTES
# -----------------------------
@app.get("/")
async def root():
    return {"message": "API is running"}

@app.get("/test-db")
async def test_db():
    user_count = await users_col.count_documents({})
    section_count = await sections_col.count_documents({})
    task_count = await tasks_col.count_documents({})
    return {
        "users": user_count,
        "sections": section_count,
        "tasks": task_count
    }

# --- TASKS ---
@app.get("/tasks")
async def get_tasks():
    tasks = []
    async for t in tasks_col.find():
        t["_id"] = str(t["_id"])
        tasks.append(t)
    return tasks

@app.post("/tasks")
async def create_task(task: TaskModel):
    new_task = task.dict()
    result = await tasks_col.insert_one(new_task)
    new_task["_id"] = str(result.inserted_id)
    return new_task

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    result = await tasks_col.delete_one({"_id": ObjectId(task_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted"}

@app.put("/tasks/{task_id}")
async def update_task(task_id: str, task: TaskModel):
    result = await tasks_col.update_one(
        {"_id": ObjectId(task_id)},
        {"$set": task.dict()}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task updated"}

# --- SECTIONS ---
@app.get("/sections")
async def get_sections():
    sections = []
    async for s in sections_col.find():
        s["_id"] = str(s["_id"])
        sections.append(s)
    return sections

@app.post("/sections")
async def create_section(section: SectionModel):
    new_section = section.dict()
    result = await sections_col.insert_one(new_section)
    new_section["_id"] = str(result.inserted_id)
    return new_section

@app.delete("/sections/{section_id}")
async def delete_section(section_id: str):
    result = await sections_col.delete_one({"_id": ObjectId(section_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Section not found")
    return {"message": "Section deleted"}
