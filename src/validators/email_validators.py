from src.database.session import get_session
from src.models.user_model import User
from sqlalchemy import select
import email_validator

def email_already_exists(verifying_email):
    stmt = select(User.email).where(User.email == verifying_email)
    
    with get_session() as session:
        result = session.scalar(stmt)
        
    return result != None


def verify_email(email):
    try:
        email_validator.validate_email(email)
        return True
    except email_validator.EmailNotValidError:
        return False
