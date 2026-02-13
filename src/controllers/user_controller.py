from models.user_model import User
from database.session import get_session
from sqlalchemy import select
from argon2 import PasswordHasher

argon2 = PasswordHasher()


def create_user(new_real_name, new_username, new_email, new_password):
    new_user = User(
        real_name=new_real_name,
        username=new_username,
        email=new_email,
        password=argon2.hash(new_password)
        )

    with get_session() as session:
        session.add(new_user)
        
