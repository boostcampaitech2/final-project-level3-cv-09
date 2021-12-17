from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from model import model, schemas
import csv

# get food by name
def get_food(name: str, db: Session):
    return db.query(model.Foods).filter(model.Foods.name == name).first()

def get_food_list(skip: int, limit: int, db: Session):
    foods = db.query(model.Foods).offset(skip).limit(limit).all()
    return foods

# insert feed back
def get_user_feedback_image(db: Session, skip: int=0, limit: int=100):
    return db.query(model.UserFeedbackImage).offset(skip).limit(limit).all()

def get_user_feedback_image_row_count(db: Session):
    return db.query(model.UserFeedbackImage).count()

def get_user_feedback_image_by_id(id: int, db: Session):
    return db.query(model.UserFeedbackImage).filter(model.UserFeedbackImage.id == id).first()

def get_user_feedback_food(db: Session, skip: int=0, limit: int=100):
    return db.query(model.UserFeedbackFood).offset(skip).limit(limit).all()

def get_user_feedback_food_by_id(id: int, db: Session):
    return db.query(model.UserFeedbackFood).filter(model.UserFeedbackFood.id == id).first()

def get_user_feedback_by_img_id(db:Session, img_id: int):
    db_user_feedback = db.query(model.UserFeedbackImage).filter(model.UserFeedbackImage.id ==img_id).first()
    if db_user_feedback is None:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user_feedback

def create_user_feedback_image(db: Session, user_feedback_image: schemas.UserFeedbackImageBase):
    db_user_feedback_image = model.UserFeedbackImage(
        date_time = user_feedback_image.date_time,
        img_path = user_feedback_image.img_path
    )
    db.add(db_user_feedback_image)
    db.commit()
    db.refresh(db_user_feedback_image)
    
    return db_user_feedback_image.id

def create_user_feedback_food(db:Session, user_feedback_food: schemas.UserFeedbackFoodBase, img_id: int):
    db_user_feedback_food = model.UserFeedbackFood(
        predict_bbox = user_feedback_food.predict_bbox,
        feedback = user_feedback_food.feedback,
        img_id = img_id
    )
    db.add(db_user_feedback_food)
    db.commit()
    db.refresh(db_user_feedback_food)

    return db_user_feedback_food.id

# init db
def init_db(db: Session):
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
            
            db_food = model.Foods(**{"name_ko":ko_name, "name":name, "serving_size":serving_size, "kcal":kcal, "tan":tan, "dan":dan, "gi":gi, "na":na})
            print(db_food)

            db.add(db_food)
            
            db.commit()
            db.refresh(db_food)