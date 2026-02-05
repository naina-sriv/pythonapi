import jwt
from jwt import PyJWTError
import datetime
#secret key
#algo
#expiration time
# bash$ openssl rand -hex 32
SECRET_KEY="0fd9ce0ac69b895b92847b6deda8152cc0db9fd414eb1d7c3da28cc829c443be"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES= 30

def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.datetime.now()+datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
    
    