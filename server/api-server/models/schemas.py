from typing import List, Optional

from pydantic import BaseModel

class Food(BaseModel):
    name : str
    name_ko : str
    serving_size: str
    kcal : float
    tan : float
    dan : float
    gi : float
    na : float
    
    class Config:
        orm_mode = True

class Diet(BaseModel):
    date: str
    image: str
    food_list:List[Food] = []
