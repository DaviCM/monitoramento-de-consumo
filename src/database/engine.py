from base import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("", echo=True) # Colocar o caminho aqui

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


