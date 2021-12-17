import os
import base64

from io import BytesIO
from PIL import Image
from sqlalchemy.orm import Session

from dao import dao
from model import model, schemas

feedback_image_path = "images/feedback"

def post_user_feedback(user_feedback:schemas.RequestUserFeedback ,db: Session):
    
    # save image
    img_path = os.path.join(feedback_image_path, f"{str(dao.get_user_feedback_image_row_count(db) + 1)}.jpg")

    img = Image.open(BytesIO(base64.b64decode(user_feedback.img)))
    img.save(img_path)

    # create user feedback image
    
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
    
    return img_id