from fastapi import APIRouter, Depends, status, HTTPException
from src.core.database import get_db
from sqlmodel import Session
from src.core.models import User
from src.library.books.services import (
    fetch_requests, 
    process_requests, 
    fetch_user_history, 
    list_books, 
    borrow_request, 
    fetch_personal_history,
    add_book,
    create_borrow_request,
    return_book
)
from src.utils.rbac import verify_librarian, verify_user, get_current_user
from .schemas import BorrowRequest, BookResponse, BookCreateSchema, BorrowRequestCreate, BorrowApproved, Request_Out, BorrowHistoryResponse
from typing import List


router_user = APIRouter()

# User Routes

@router_user.get("/books", dependencies= [Depends(verify_user)],status_code=status.HTTP_200_OK, response_model=List[BookResponse])
async def get_books(db = Depends(get_db)):
    return list_books(db)


# @router.post("/borrow",  dependencies= [Depends(verify_user)])
# async def borrow_request(borrow : BorrowRequest, db =Depends(get_db)):
#     return borrow_request(borrow, db)

@router_user.get("/{user_id}/history",  dependencies= [Depends(verify_user)])
async def personal_history(user_id, db = Depends(get_db)):
    return fetch_personal_history(user_id, db)


@router_user.post("/borrow", response_model=BorrowRequestCreate)
async def borrow_book(
    borrow_request: BorrowRequestCreate,
    db: Session = Depends(get_db),
    current_user_id = Depends(get_current_user),  
):
    try:
        new_borrow_request = create_borrow_request(borrow_request, db, current_user_id)
        return new_borrow_request
    except HTTPException as e:
        raise e
    
@router_user.post("/return/{borrow_id}", response_model= BorrowHistoryResponse)
def return_book(borrow_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    try:
        return_history  = return_book(borrow_id , current_user, db)
        return return_history
    
    except HTTPException as e:
        raise e