import os
from src.database.base import Base
from src.models.consumption_history_model import ConsumptionHistory
from src.models.consumption_simulation_model import ConsumptionSimulation
from src.models.goal_model import Goal
from src.models.tip_model import Tip
from src.models.user_model import User
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

# psycopg: driver python para postgres
# apenas pip install psycopg não é suficiente, devemos instalar também a versão compilada para evitar erros.

# Aqui será criada a engine e será feita a pool de sessões, onde todas as sessões disponíveis estão
engine = create_engine(url=os.getenv('DATABASE_URL'),
                       pool_size=int(os.getenv('DATABASE_POOL_SIZE')), # Tamanho máximo de conexões simultâneas disponíveis no sistema
                       max_overflow=int(os.getenv('DATABASE_MAX_OVERFLOW')), # Conexões possíveis acima do tamanho da pool (pico temporário)
                       pool_pre_ping=True, # Verifica a integridade da conexão sempre que a sessão é iniciada
                       echo=True)

if __name__ == '__main__':
    Base.metadata.create_all(checkfirst=True,
                             bind=engine)