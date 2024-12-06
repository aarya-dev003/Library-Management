from fastapi import APIRouter, Depends, status
from src.auth.schemas import UserCreate, UserLogin, UserResponse
from src.auth.services import create_user, authenticate_user
from src.core.database import get_db
from src.utils.rbac import verify_librarian

router = APIRouter()

@router.post('/register', dependencies=[Depends(verify_librarian)], status_code= status.HTTP_201_CREATED, response_model = UserResponse)
async def register(user: UserCreate, db = Depends(get_db)):
    return create_user(user, db)

@router.post('/login')
async def login (user: UserLogin, db = Depends(get_db)):
    return authenticate_user(user, db)