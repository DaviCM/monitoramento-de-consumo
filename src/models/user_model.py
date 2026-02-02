from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.base import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    real_name = Column(String(120), nullable=False)
    username = Column(String(120), nullable=False, unique=True)
    email = Column(String(120), nullable=False, unique=True)
    password = Column(String(255), nullable=False)

    user_consumption_history = relationship('ConsumptionHistory', back_populates='goals.creator_id')
    user_consumption_simulations = relationship('ConsumptionSimulation', back_populates='goals.creator_id')
    user_goals = relationship('Goal', back_populates='goals.creator_id')
    
    
    
    