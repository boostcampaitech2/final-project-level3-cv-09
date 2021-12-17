from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import uvicorn
from model import model, schemas
from database import SessionLocal, engine
from dao import dao
from model.schemas import RequestPrediction
from predict import predict
import os

image_path = "/images/feedback"

model.Base.metadata.create_all(bind=engine)

def get_application() -> FastAPI:
    application = FastAPI()

    return application

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = get_application()

# inference api
@app.post("/api/v1/inference")
def requests_prediction(requests : RequestPrediction, db: Session = Depends(get_db)):
    img = requests.img
    date_time = requests.date_time
    print(date_time, len(img))
    # start inference
    pre = predict.Prediction(img)
    outputs = pre.inference()

    status = "success" if len(outputs) > 0 else "fail"
    print(outputs)

    # parsing & read from db
    food_list = []
    for out in outputs:
        cls = out["class"]
        name = out["name"]
        bbox = out["bbox"]
        food = dao.get_food(name, db)
        response_food = schemas.ResponseFood(
            **{
                "name":food.name, 
                "name_ko":food.name_ko, 
                "serving_size":food.serving_size, 
                "cls":cls,
                "kcal":food.kcal, 
                "tan":food.tan, 
                "dan":food.dan,
                "gi":food.gi, 
                "na":food.na, 
                "bbox":bbox
            }
        )
        food_list.append(response_food)
    response_diet = schemas.ResponseDiet(
        **{
            "status": status,
            "date_time":date_time,
            "food_list":food_list
        }
    )
    response_prediction = schemas.ResponsePediction(diet = response_diet)

    return response_prediction

@app.get("/api/v1/private/foods", response_model=List[schemas.Food])
def get_food_list(skip: int=0, limit: int=100, db: Session = Depends(get_db)):
    food_list = dao.get_food_list(skip, limit, db)
    return food_list

@app.get("/api/v1/private/init_db")
def init_database(db: Session = Depends(get_db)):
    dao.init_db(db)

@app.get("/api/v1/feedback/foods", response_model=List[schemas.UserFeedbackFood])
def get_user_feedback_foods(skip: int=0, limit: int=100, db: Session = Depends(get_db)):
    return dao.get_user_feedback_food(db, skip, limit)

@app.get("/api/v1/feedback/foods/{id}", response_model=schemas.UserFeedbackFood)
def get_user_feedback_food_by_id(id: int, db: Session = Depends(get_db)):
    return dao.get_user_feedback_food_by_id(id, db)

@app.get("/api/v1/feedback/image", response_model=List[schemas.UserFeedbackImage])
def get_user_feedback_images(skip: int=0, limit: int=100, db: Session = Depends(get_db)):
    return dao.get_user_feedback_image(db, skip, limit)

@app.get("/api/v1/feedback/image/{id}", response_model=schemas.UserFeedbackImage)
def get_user_feedback_image_by_id(id: int, db: Session = Depends(get_db)):
    return dao.get_user_feedback_image_by_id(id, db)

@app.get("/api/v1/feedback/{img_id}", response_model=schemas.UserFeedback)
def get_user_feedback_by_img_id(img_id: int, db: Session = Depends(get_db)):
    return dao.get_user_feedback_by_img_id(db, img_id)

@app.post("/api/v1/feedback")
def post_user_feedback(user_feedback:schemas.RequestUserFeedback ,db: Session = Depends(get_db)):
    
    # create user feedback image
    img_path = os.path.join(image_path, str(dao.get_user_feedback_image_row_count(db)), ".jpg")
    user_feedback_image = schemas.UserFeedbackImageBase(
        date_time = user_feedback.date_time,
        img_path = img_path
    )

    img_id = dao.create_user_feedback_image(db, user_feedback_image)

    # create user feedback food
    for food, feedback in zip(user_feedback.food_list, user_feedback.feedback):
        predict_bbox = " ".join([str(bbox) for bbox in food.bbox])
        print(predict_bbox)
        user_feedback_food = schemas.UserFeedbackFoodBase(
            predict_bbox = predict_bbox,
            feedback = feedback
        )
        id = dao.create_user_feedback_food(db, user_feedback_food, img_id)
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
