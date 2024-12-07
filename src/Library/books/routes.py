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


router = APIRouter()



@router.get('/requests', dependencies= [Depends(verify_librarian)], status_code=status.HTTP_200_OK)
async def view_borrow_requests(db = Depends(get_db)):
    return fetch_requests(db)

@router.put("/requests/{request_id}",dependencies= [Depends(verify_librarian)], response_model= Request_Out)
async def handle_borrow_request(request_id : int, action : BorrowApproved, db = Depends(get_db)):
    return process_requests(request_id, action, db)

@router.get("/{user_id}/history",dependencies= [Depends(verify_librarian)])
async def user_history(user_id : int, db = Depends(get_db)):
    return fetch_user_history(user_id, db)

@router.post("/books", dependencies= [Depends(verify_librarian)], status_code=status.HTTP_201_CREATED, response_model = BookCreateSchema)
async def add_books(book : BookCreateSchema, db = Depends(get_db)):
    try:
        return add_book(db = db,book= book)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error adding book : {e} ")





