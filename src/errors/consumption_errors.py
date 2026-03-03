from app_error import AppError
from fastapi import status

class InvalidDateError(AppError):
    status_code = status.HTTP_400_BAD_REQUEST
    status_name = 'INVALID_DATE'
    message = 'A data que você tentou inserir é inválida ou nula. Por favor, insira um valor válido.'
    


class InvalidConsumptionValueError(AppError):
    status_code = status.HTTP_400_BAD_REQUEST
    status_name = 'INVALID_CONSUMPTION_VALUE'
    message = 'O valor do consumo você tentou inserir é inválido ou nulo. Por favor, insira um valor válido.'
    
    

class ConsumptionsNotFoundError(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    status_name = 'CONSUMPTIONS_NOT_FOUND'
    message = 'Não foi encontrado nenhum consumo. Por favor, tente novamente.'
    
    
    
class SimulationsNotFoundError(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    status_name = 'SIMULATIONS_NOT_FOUND'
    message = 'Não foi encontrada nenhuma simulação. Por favor, tente novamente.'
    
    
    
class GoalsNotFoundError(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    status_name = 'GOALS_NOT_FOUND'
    message = 'Não foi encontrado nenhuma meta. Por favor, tente novamente.'
    
    
    