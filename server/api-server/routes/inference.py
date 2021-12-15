from fastapi import APIRouter
router = APIRouter(prefix='/inference')

@router.post('/')
def inference_request():
    return {"predict":"yolov5"}

@router.get('/foods')
def get_food_list():
    return 