from sqlalchemy.orm import sessionmaker
from src.database.engine import engine

def pegar_sessao():
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        yield session
    finally:
        session.close()
