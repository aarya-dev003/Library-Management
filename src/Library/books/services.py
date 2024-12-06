from sqlalchemy.orm import Session
from src.core import models
from src.library.books import schemas
from fastapi import HTTPException, status
from src.core.models import User



#  librarian service

def fetch_requests(db: Session):
    return db.query(models.BorrowRequest).filter(models.BorrowRequest.status == "pending").all()

def process_requests(request_id : int, action : str, db: Session):
    request = db.query(models.BorrowRequest).filter(models.BorrowRequest.id == request_id).first()

    if not request:
        return f"Request with Id {request_id} not Found"

    if action == "approve":
        request.status = "approved"

        borrow_history = models.BorrowHistory(
            book_id= request.book_id,
            user_id = request.user_id,
            borrow_date= request.borrow_start_date,
            return_date= request.return_date
        )



    elif action == "reject":
        request.status = "rejected"
    
    else:
        return "Invalid Operation"
    
    db.commit()
    db.refresh(request)

    return request


def fetch_user_history(user_id : int , db : Session):
    history = db.query(models.BorrowHistory).filter(models.BorrowHistory.user_id == user_id).all()
    return history



# User Services

def list_books(db: Session):
    return db.query(models.Book).all()

def borrow_request(borrow_req : schemas.BorrowRequest ,db: Session):
    user =  db.query(User).filter(User.id == borrow_req.user_id).first()
    book = db.query(models.Book).filter(models.Book.id == borrow_req.book_id).first()

    if not user or not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not Found")
    
    if book.available == False:
        return {
            "message" : "Book Not Available"
        }
    

    borrow_request =  models.BorrowRequest(
        user_id= borrow_req.user_id,
        book_id=borrow_req.book_id,
        borrow_start_date=borrow_req.start_date,
        return_date=borrow_req.end_date
    )


    db.add(borrow_request)
    db.commit()
    db.refresh(borrow_request)

    book.available = False
    db.add(book)
    db.commit()

    return {
        "message" : "Borrow request Submitted",
        "request" : borrow_request
    }
    

def fetch_personal_history(user_id : int, db: Session):
    return db.query(models.BorrowHistory).filter(models.BorrowHistory.user_id == user_id).all()