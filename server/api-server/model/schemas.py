from typing import List, Optional
from pydantic import BaseModel

class FoodBase(BaseModel):
    name : str
    name_ko : str
    serving_size: str
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

class RequestPrediction(BaseModel):
    img : str
    date_time : str

class ResponsePediction(BaseModel):
    date_time: str
    food_list : List[ResponseFood]
