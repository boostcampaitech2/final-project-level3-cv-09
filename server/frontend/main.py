import re
import requests
import streamlit as st
import os
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

def draw_box(image, bbox, feedback=True):
    size = image.size

    minx, miny, maxx, maxy = map(float, bbox.split())
    minx *= size[0]
    maxx *= size[0]

    miny *= size[1]
    maxy *= size[1]
    fill = (0, 0, 255) if feedback else (255, 0, 0)

    draw = ImageDraw.Draw(image)
    draw.rectangle(((minx, miny), (maxx, maxy)), outline=fill, width=3)

    return image

def init():
    st.title("FoodLog Monitoring Page")
    feedback_list = requests.get("http://localhost:8000/api/v1/feedback/image").json()

    for feedback in feedback_list:
        img = Image.open(os.path.join('../backend', feedback['img_path']))
        # st.write()
        user_feedback_food = requests.get(f"http://localhost:8000/api/v1/feedback/{feedback['id']}").json()

        with st.expander(f"이미지 경로: {feedback['img_path']} \n 요청 시간: {feedback['date_time']}", expanded=False):

            for item in user_feedback_food["items"]:
                img = draw_box(img, item["predict_bbox"], item["feedback"])

            message = '<p style="color:Blue; font-size: 14px; text-align: right;">예측 성공</p>' + '<p style="color:Red; font-size: 14px; text-align:right;">사용자 피드백(오탐)</p>'
            st.markdown(message, unsafe_allow_html=True)

            st.image(img, str(img.size))


if __name__ == "__main__":
    init()