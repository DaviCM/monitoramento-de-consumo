from database.session import get_session
from sqlalchemy import select
from argon2 import PasswordHasher
from re import Match
import re

argon2 = PasswordHasher()

def verify_password_veracity(hashed_password, password):
    return argon2.verify(hashed_password, password)
