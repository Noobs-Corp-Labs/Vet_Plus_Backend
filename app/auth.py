from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

# DEV: Define as funcs de Validação, Autenticação, Etc relacionadas ao Token
def get_current_user(token: str = Depends(oauth2_scheme)):
    return {'user': 'demo'}

def get_current_admin_user(token: str = Depends(oauth2_scheme)):
    return {'user': 'admin'}
