from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from src.core.config import settings


SECRET_KEY  = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES



pwd_context = CryptContext(schemes=["argon2"], deprecated = "auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password : str , hash_password: str) -> bool:
    return pwd_context.verify(password,hash_password)

def create_access_token(data : dict, expires: timedelta = None) -> str:
    to_encode = data.copy()
    if expires:
        expire = datetime.now() + expires
    else:
        expire = datetime.now() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES) 
    
    to_encode.update({
        "exp" : expire
    })

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
