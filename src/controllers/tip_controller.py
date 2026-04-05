from src.models.tip_model import Tip
from src.database.session import get_session
from src.errors.tip_errors import TipsNotFoundError
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from random import choice
import json

def create_tips():
    with open('src/editors/new_tips.json', 'r', encoding='utf-8') as file:
        new_tips: list = json.load(file)

        # for tip in new_tips:
        #     print(tip['si_measurement_unit'], tip['tip'])

        # print(type(new_tips))

    with get_session() as session:
        for tip_dict in new_tips:
            try:
                new_tip = Tip(
                    si_measurement_unit=(tip_dict['si_measurement_unit']).lower(),
                    tip=tip_dict['tip']
                    )

                session.add(new_tip)
                # Adiciona a dica antes do commit, e assim pode capturar o IntegrityError
                session.flush() 
                
            except IntegrityError:
                session.rollback()
                print(f'Essa dica foi ignorada por já estar no banco de dados: ({tip_dict['tip']})')
                continue


def get_tip(measurement_unit):
    stmt = select(Tip).where(Tip.si_measurement_unit == (measurement_unit.lower()))
    
    with get_session() as session:
        result = session.scalars(stmt).all()
        
    if result == []:
        raise TipsNotFoundError
    
    # Escolhe aleatoriamente uma dica da lista retornada pelo scalars()    
    return choice(result)


if __name__ == '__main__':
    create_tips()