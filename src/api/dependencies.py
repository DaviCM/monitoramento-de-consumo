from sqlalchemy.orm import sessionmaker
from database import engine

def pegar_sessao():
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        yield session
    finally:
        session.close()
