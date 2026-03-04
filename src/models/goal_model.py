from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey, func
from sqlalchemy.orm import relationship
from src.database.base import Base

class Goal(Base):
    __tablename__ = 'goals'

    id = Column(Integer, primary_key=True)
    starting_date = Column(Date, nullable=False)
    ending_date = Column(Date, nullable=False)
    si_measurement_unit = Column(String(50), nullable=False)
    value = Column(Numeric(precision=10, scale=2), default=0)

    creator_id = Column(ForeignKey('users.id', ondelete='cascade'))
    creator = relationship('User', back_populates='users.id')

    