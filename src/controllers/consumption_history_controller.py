from models.consumption_history_model import ConsumptionHistory
from models.user_model import User
from database.session import get_session
from datetime import date
from decimal import Decimal
from sqlalchemy import session

def create_consumption(current_user: User, starting_date: date, ending_date: date, si_measurement_unit, value: Decimal):
    pass

