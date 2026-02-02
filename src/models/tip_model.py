from sqlalchemy import Column, Integer, String
from database.base import Base

class Tip(Base):
    __tablename__ = 'tips'

    id = Column(Integer, primary_key=True)
    tip = Column(String(280), nullable=False)

    