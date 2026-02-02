import os
from base import Base
from models.consumption_history_model import ConsumptionHistory
from models.consumption_simulation_model import ConsumptionSimulation
from models.goal_model import Goal
from models.tip_model import Tip
from models.user_model import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# psycopg: driver python para postgres
# apenas pip install psycopg não é suficiente, devemos instalar também a versão compilada para evitar erros.
engine = create_engine(os.getenv('DATABASE_URL'),
                       echo=True) # Colocar o caminho aqui

Session = sessionmaker(bind=engine)
session = Session()


