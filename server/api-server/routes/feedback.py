from fastapi import APIRouter

router = APIRouter(prefix="/feedback")

@router.post("/", tags=["feedback"])
def feedback_request():
    return {"feedback:users"}