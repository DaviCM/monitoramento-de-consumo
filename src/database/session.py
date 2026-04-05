# Tentativa de criar uma espécie de 'pool' de sessões com base em contexto, distrubíndo elas para cada regra de negócio
from src.database.engine import engine
from src.errors.app_errors import AppError, ServerSideError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi.exceptions import FastAPIError
from contextlib import contextmanager

Session = sessionmaker(bind=engine,
                       expire_on_commit=False)

# Essa função é um gerador de context-managers (with), e estabelece o que deve acontecer sempre que uma sessão é requerida pela controller
# É uma função fábrica, e o decorador serve para sinalizar que a função gera context managers, sem estar dentro de uma classe dedicada.
@contextmanager
def get_session():
    session = Session()
    try:
        yield session
        session.commit()
        
    except IntegrityError:
        session.rollback()
        raise ServerSideError('Uma restrição do banco de dados foi levantada, como (nullable) ou (unique). Verifique as últimas manipulações de dados.')
    
    except SQLAlchemyError:
        session.rollback()
        raise ServerSideError('Uma exceção a nível de servidor aconteceu. Verifique se a conexão está funcionando e se o banco de dados está inicializado.')
    
    except FastAPIError:
        session.rollback()
        raise ServerSideError('Uma exceção no funcionamento da API aconteceu, verifique se todo o código está ok.')
    
    except AppError:
        session.rollback()
        raise
    
    except Exception as e:
        session.rollback()
        raise e
    
    finally:
        session.close()

