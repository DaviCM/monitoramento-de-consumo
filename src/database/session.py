# Tentativa de criar uma espécie de 'pool' de sessões com base em contexto, distrubíndo elas para cada regra de negócio
from engine import engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

Session = sessionmaker(bind=engine)

# Essa função é um gerador de context-managers (with), e estabelece o que deve acontecer sempre que uma sessão é requerida pela controller
# É uma função fábrica, e o decorador serve para sinalizar que a função gera context managers, sem estar dentro de uma classe dedicada.
@contextmanager
def get_session():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

