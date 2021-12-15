from sqlalchemy import Column, String, Float, Integer
from database import Base

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





