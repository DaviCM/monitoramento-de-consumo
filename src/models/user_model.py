from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from src.database.base import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    real_name = Column(String(120), nullable=False)
    username = Column(String(120), nullable=False, unique=True)
    email = Column(String(120), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    user_consumption_history = relationship('ConsumptionHistory', back_populates='goals.creator_id')
    user_consumption_simulations = relationship('ConsumptionSimulation', back_populates='goals.creator_id')
    user_goals = relationship('Goal', back_populates='goals.creator_id')
    
    
    
    