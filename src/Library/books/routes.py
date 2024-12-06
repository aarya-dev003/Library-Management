from fastapi import APIRouter, Depends, status
from src.core.database import get_db
from src.library.books.services import fetch_requests, process_requests, fetch_user_history, list_books, borrow_request, fetch_personal_history
from src.utils.rbac import verify_librarian, verify_user
from .schemas import BorrowRequest, BookResponse
from typing import List


router = APIRouter()


# Librarian Routes

@router.get('/requests', dependencies= [Depends(verify_librarian)], status_code=status.HTTP_200_OK)
async def view_borrow_requests(db = Depends(get_db)):
    return fetch_requests(db)

@router.put("/requests/{request_id}",dependencies= [Depends(verify_librarian)])
async def handle_borrow_request(request_id : int, action : str, db = Depends(get_db)):
    return process_requests(request_id, action, db)

@router.get("/user/{user_id}/history",dependencies= [Depends(verify_librarian)])
async def user_history(user_id : int, db = Depends(get_db)):
    return fetch_user_history(user_id, db)


# User Routes

@router.get("/books", dependencies= [Depends(verify_user)],status_code=status.HTTP_200_OK, response_model=List[BookResponse])
async def get_books(db = Depends(get_db)):
    return list_books(db)

@router.post("/borrow",  dependencies= [Depends(verify_user)])
async def borrow_request(borrow : BorrowRequest, db =Depends(get_db)):
    return borrow_request(borrow, db)

@router.get("/history",  dependencies= [Depends(verify_user)])
async def personal_history(user_id, db = Depends(get_db)):
    return fetch_personal_history(user_id, db)
