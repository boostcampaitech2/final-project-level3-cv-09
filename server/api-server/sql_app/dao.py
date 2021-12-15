from sqlalchemy.orm import Session
from model import model
import csv

# get food by name
def get_food(name: str, db: Session):
    return db.query(model.Foods).filter(model.Foods.name == name).first()

def get_food_list(skip: int, limit: int, db: Session):
    foods = db.query(model.Foods).offset(skip).limit(limit).all()
    return foods

# insert feed back

# insert history 

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