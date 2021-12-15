from pydantic import BaseModel
from typing import Optional

# Inference 결과를 반환하는 VO
class InferenceResponse(BaseModel):
    pass

class Food(BaseModel):
    pass

class InferenceRequst(BaseModel):
    img:str