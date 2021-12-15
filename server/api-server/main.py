from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import uvicorn
from routes import feedback, inference
from models import models, schemas
from database import SessionLocal, engine
import csv


models.Base.metadata.create_all(bind=engine)

def get_application() -> FastAPI:
    application = FastAPI()
    application.include_router(feedback.router)
    application.include_router(inference.router)

    return application

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = get_application()

@app.get("/hello")
def hello():
    return {
        "message": "world!"
    }
    
@app.get("/foods", response_model=List[schemas.Food])
def read_foods(skip: int=0, limit: int=100, db: Session = Depends(get_db)):
    foods = db.query(models.Foods).offset(skip).limit(limit).all()
    return foods

@app.get("/init_db")
def init_database(db: Session = Depends(get_db)):
    print("start init Database")

    with open('./nutrition.csv', 'r', newline='', encoding='utf8') as csv_file:
        reader = csv.reader(csv_file)
        
        for i, line in enumerate(reader):
            if i == 0:
                continue
            print(line)
            ko_name, name, serving_size, kcal, tan, dan, gi, na = line
            kcal = float(kcal[:-5])
            tan = float(tan[:-1])
            dan = float(dan[:-1])
            gi = float(gi[:-1])
            na = float(na[:-2])
            
            db_food = models.Foods(**{"name_ko":ko_name, "name":name, "serving_size":serving_size, "kcal":kcal, "tan":tan, "dan":dan, "gi":gi, "na":na})
            print(db_food)

            db.add(db_food)
            
            db.commit()
            db.refresh(db_food)
            # break

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
