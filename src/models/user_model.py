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

    user_consumption_history = relationship('ConsumptionHistory', back_populates='creator', cascade='all, delete-orphan', passive_deletes=True)
    user_consumption_simulations = relationship('ConsumptionSimulation', back_populates='creator', cascade='all, delete-orphan', passive_deletes=True)
    user_goals = relationship('Goal', back_populates='creator', cascade='all, delete-orphan', passive_deletes=True)
    
    
# cascade='all, delete 'orphan' diz ao SQLAlchemy para sempre deletar consumos quando o usuário for deletado, e deletar consumos que não possuem um usuário associado.
# passive_deletes=True significa que o SQLAlchemy delega a deleção ao banco, não faz isso manualmente.
    