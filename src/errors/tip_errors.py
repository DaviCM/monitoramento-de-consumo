from src.errors.app_errors import AppError
from fastapi import status

class TipsNotFoundError(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    status_name = 'TIPS_NOT_FOUND'
    message = 'Nenhuma dica foi encontrada para essa unidade de medida.'