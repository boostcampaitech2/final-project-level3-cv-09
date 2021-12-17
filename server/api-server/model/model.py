from sqlalchemy import Column, String, Float, Integer, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from database import Base

# Food Nutrition DB Table

class Foods(Base):
    __tablename__ = 'foods'

    name = Column(String(100), primary_key=True)
    name_ko = Column(String(100),  nullable=False)
    serving_size = Column(String(100), nullable=True)
    kcal = Column(Float())
    tan = Column(Float())
    dan = Column(Float())
    gi = Column(Float())
    na = Column(Float())

# User Feedback DB Tables

class UserFeedbackImage(Base):
    __tablename__ = 'user_feedback_image'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    date_time = Column(String(100), nullable=False)
    img_path = Column(String(200), nullable=False)

    items = relationship("UserFeedbackFood", back_populates="owner")

class UserFeedbackFood(Base):
    __tablename__ = 'user_feedback_food'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    predict_bbox = Column(String(100), nullable=False)
    feedback = Column(Boolean, default=True, nullable=False)
    img_id = Column(Integer, ForeignKey("user_feedback_image.id"))

    owner = relationship("UserFeedbackImage", back_populates="items")



