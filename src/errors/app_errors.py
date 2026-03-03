from fastapi import status

class AppError(Exception):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    status_name = 'INTERNAL_SERVER_ERROR'
    message = 'Um erro de servidor ocorreu. Desculpe o transtorno!'



class ServerSideError(Exception):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    status_name = 'SERVER_SIDE_ERROR'
    
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)