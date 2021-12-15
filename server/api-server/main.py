from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import uvicorn
from model import model, schemas
from database import SessionLocal, engine
from sql_app import dao
from model.schemas import RequestPrediction
from predict import predict

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
@app.post("/inference")
def requests_prediction(requests : RequestPrediction, db: Session = Depends(get_db)):
    img = requests.img
    date_time = requests.date_time
    
    # start inference
    pre = predict.Prediction(img)
    outputs = pre.inference()

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
                "kcal":food.kcal, 
                "tan":food.tan, 
                "dan":food.dan,
                "gi":food.gi, 
                "na":food.na, 
                "bbox":bbox
            }
        )
        food_list.append(response_food)
    print(type(food_list))
    response_prediction = schemas.ResponsePediction(
        **{
            "date_time":date_time,
            "food_list":food_list
        }
    )

    return response_prediction

@app.get("/foods", response_model=List[schemas.Food])
def get_food_list(skip: int=0, limit: int=100, db: Session = Depends(get_db)):
    food_list = dao.get_food_list(skip, limit, db)
    return food_list

@app.get("/init_db")
def init_database(db: Session = Depends(get_db)):
    dao.init_db(db)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
