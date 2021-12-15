from fastapi import APIRouter
from model.schemas import RequestPrediction, ResponsePediction, ResponseFood
from predict import predict
from sqlalchemy.orm import Session
from model import model
# router = APIRouter(prefix='/inference')

# @router.post('/inference')
# def requests_prediction(requests : RequestPrediction):
#     img = requests.img
#     date_time = requests.date_time

#     # start inference
#     pre = predict.Prediction(img)
#     outputs = pre.inference()

#     # parsing & read from db
#     for out in outputs:

#         cls = out["class"]
#         name = out["name"]
#         bbox = out["bbox"]

    
#     return {"predict":"yolov5"}

