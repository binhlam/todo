from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='/auth/signin')

SECRECT_KEY = '4e5443c8495db2010f69d7828b61f2c71d5f2030c740217143f841f352550f0a'
ALGORITHM = 'HS256'
