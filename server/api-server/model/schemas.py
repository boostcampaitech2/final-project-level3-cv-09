from typing import List, Optional
from pydantic import BaseModel

# Inference Schemas

class FoodBase(BaseModel):
    name : str
    name_ko : str
    serving_size: str
    cls : int
    kcal : float
    tan : float
    dan : float
    gi : float
    na : float

class Food(FoodBase):

    class Config:
        orm_mode = True

class ResponseFood(FoodBase):
    bbox : List[float]

class RequestFood(FoodBase):
    bbox: List[float]

class RequestPrediction(BaseModel):
    img : str
    date_time : str

class ResponseDiet(BaseModel):
    status:str
    date_time: str
    food_list: List[ResponseFood]

class ResponsePediction(BaseModel):
    diet: ResponseDiet

# User Feedback Schemas

class UserFeedbackImageBase(BaseModel):
    date_time: str
    img_path: str

class UserFeedbackImage(UserFeedbackImageBase):
    id: int
    class Config:
        orm_mode = True

class UserFeedbackFoodBase(BaseModel):
    predict_bbox: str
    feedback : bool

class UserFeedbackFood(UserFeedbackFoodBase):
    id: int
    class Config:
        orm_mode = True

class UserFeedback(UserFeedbackImageBase):
    id: int
    items: List[UserFeedbackFood]
    class Config:
        orm_mode = True

class RequestUserFeedback(BaseModel):
    img: str
    date_time: str
    food_list: List[RequestFood]
    feedback: List[bool]


