from src.core.security import hash_password, verify_password, create_access_token
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.auth.schemas import UserCreate, UserResponse, UserLogin, TokenData
from src.core.models import User

def create_user(user: UserCreate, db : Session) -> UserResponse:
    existing = db.query(User).filter(User.email == user.email).first()

    if existing : 
        raise HTTPException(status_code=400, detail="Email Already Exists")
    
    hashed_pswd = hash_password(user.password)

    new_user = User(
        email = user.email,
        hashed_password = hashed_pswd
    )

    db.add(new_user)
    db.commit()

    db.refresh(new_user)

    return UserResponse(
        email= new_user.email,
        id = new_user.id,
        role = new_user.role
    )


def authenticate_user(user_data: UserLogin, db : Session) -> TokenData:
    user = db.query(User).filter(User.email == user_data.email).first()

    if not user or not verify_password(user_data.password,user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    
    token = create_access_token({
        "email" : user.email,
        "role" : user.role,
        "id" : user.id
    })

    return TokenData(
        access_token= token
    )


