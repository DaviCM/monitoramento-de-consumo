from re import Match
import re

def verify_password(password):
    # ? é um lookahead, o que significa que ele verifica um padrão para os caracteres à frente.
    # Nesse caso, cada lookahead faz um match para verificar a existência de um caractere do respectivo grupo na expressão [].
    # . identifica que a expressão fará match de qualquer caractere indicado, pois pode haver qualquer coisa antes do conjunto [].
    # * identifica que deve haver zero ou mais caracteres desse tipo antes da expressão a ser avaliada.
    
    pattern = r"(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%&*?])[a-zA-Z0-9!@#$%&*?]{6,}$"
    result = re.match(pattern, password)
    
    return True if type(result) == Match else False