from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from jose import jwt, JWTError
from src.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def verify_role(required_role : str):
    def role_checker(token : str = Depends(oauth2_scheme)):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            if payload.get("role") != required_role:
                raise HTTPException(status_code= 403, detail="Access Denied: Insufficient Privileges")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid Token")
    
    return role_checker


verify_librarian = verify_role("librarian")
verify_user = verify_role("user")


def get_current_user(token : str = Depends(oauth2_scheme)):
    try :
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("id")
        if user_id is None:
            raise HTTPException(status_code=401, detail= "Invalid Token")
        
        return user_id
    
    except JWTError: 
        raise HTTPException(status_code=401, detail= "Invalid Token")