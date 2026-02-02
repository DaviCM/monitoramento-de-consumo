from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base

class ConsumptionHistory(Base):
    __tablename__ = 'consumption_history'   
    
    id = Column(Integer, primary_key=True)
    starting_date = Column(DateTime, nullable=False)
    ending_date = Column(DateTime, nullable=False)
    si_measurement_unit = Column(String(50), nullable=False)
    value = Column(Numeric(precision=10, scale=2), nullable=False)
    
    creator_id = Column(ForeignKey('users.id', ondelete='cascade'))
    creator = relationship('User', back_populates='users.id')
