from sqlalchemy import Column, Integer, String, Date, func
from src.database.base import Base

class Tip(Base):
    __tablename__ = 'tips'

    id = Column(Integer, primary_key=True)
    si_measurement_unit = Column(String(50), nullable=False)
    tip = Column(String(280), nullable=False, unique=True)
    created_at = Column(Date, server_default=func.now())

    