from fastapi import APIRouter, HTTPException, status
from src.models.tip_model import Tip
from src.controllers.tip_controller import get_tip
from src.schemas.tip_schemas import ResponseTipSchema
from src.errors.tip_errors import TipsNotFoundError

tip_router = APIRouter(prefix='/dicas', tags=['dicas'])

@tip_router.get(prefix='/pegar_dica_aleatoria/{unit}', status_code=status.HTTP_200_OK, response_model=ResponseTipSchema)
async def get_random_tip(unit: str):
    try: 
        return get_tip(unit)
    
    except TipsNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
        
    