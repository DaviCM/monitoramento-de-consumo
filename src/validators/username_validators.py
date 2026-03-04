from src.database.session import get_session
from src.models.user_model import User
from sqlalchemy import select
from re import Match
import re

def username_already_exists(verifying_username):
    stmt = select(User.username).where(User.email == verifying_username)
    
    with get_session() as session:
        result = session.scalar(stmt)
        return result != None


def verify_username(username):
    pattern = r"[a-zA-Z0-9][a-zA-Z0-9._]{3,15}$"
    result = re.match(pattern, username)

    return True if type(result) == Match else False

