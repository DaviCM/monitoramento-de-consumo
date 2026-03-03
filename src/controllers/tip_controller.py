from src.models.tip_model import Tip
from src.database.session import get_session
import json

with open('src/editors/new_tips.json', 'r', encoding='utf-8') as file:
    new_tips: list = json.load(file)
    
    # for tip in new_tips:
    #     print(tip['si_measurement_unit'], tip['tip'])
        
    # print(type(new_tips))
        
with get_session() as session:
    for tip_dict in new_tips:
        new_tip = Tip(
            si_measurement_unit = tip_dict['si_measurement_unit'],
            tip = tip_dict['tip']
            )
        
        session.add(new_tip)
        
