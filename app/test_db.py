from fastapi import APIRouter

router = APIRouter()

@router.get("/test")
def test_endpoint():
    return {
        "status": "success",
        "message": "Backend is working!",
        "data": {"task": "Learn FastAPI", "priority": "High"}
    }
