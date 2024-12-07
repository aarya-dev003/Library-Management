from sqlalchemy.orm import Session
from src.core import models
from src.library.books import schemas
from fastapi import HTTPException, status
from src.core.models import User
from src.library.books import schemas
from fastapi import Depends
from src.core.database import get_db
from datetime import datetime


#  librarian service

def fetch_requests(db: Session):
    return db.query(models.BorrowRequest).filter(models.BorrowRequest.status == "pending").all()

def process_requests(request_id : int, action : schemas.BorrowApproved, db: Session) -> schemas.Request_Out:
    request = db.query(models.BorrowRequest).filter(models.BorrowRequest.id == request_id).first()
    book_id = request.book_id

    book = db.query(models.Book).filter(models.Book.id == book_id).first()

    if not request:
        return f"Request with Id {request_id} not Found"

    if action.action == "approved":
        request.status = "approved"

        borrow_record = models.BorrowHistory(
            book_id= request.book_id,
            user_id = request.user_id,
            borrow_date= request.borrow_start_date,
            return_date= request.return_date,
            status= "borrowed"
        )

        book.available = False

        
        db.add(borrow_record)
        db.commit()
        db.refresh(request)




    elif action.action == "rejected":
        request.status = "rejected"
        db.commit()
        db.refresh(request)
    
    else:
        return "Invalid Operation"

    return schemas.Request_Out(
        id=request.id,
        book_id=request.book_id,
        borrow_start_date=request.borrow_start_date,
        return_date=request.return_date,
        status=request.status,
    )



def fetch_user_history(user_id : int , db : Session):
    history = db.query(models.BorrowHistory).filter(models.BorrowHistory.user_id == user_id).all()
    return history

def add_book(book : schemas.BookCreateSchema ,db: Session):
    new_book = models.Book(
        author= book.author,
        title=book.title,
        available=book.available
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    
    return new_book


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
    

def create_borrow_request(
    borrow_request_data: schemas.BorrowRequestCreate, db: Session, current_user_id
) -> schemas.BorrowRequest:
    
    book_id = borrow_request_data.book_id
    borrow_start_date = borrow_request_data.borrow_start_date
    return_date = borrow_request_data.return_date

    if borrow_start_date > return_date:
        raise HTTPException(status_code=400, detail="Return Should always be after start Date.")

    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    if not book.available:
        raise HTTPException(status_code=400, detail="Book is not available")
    
    existing_request = db.query(models.BorrowRequest).filter(
        models.BorrowRequest.book_id == book_id,
        models.BorrowRequest.user_id == current_user_id,
        models.BorrowRequest.status.in_(["pending", "approved"])
    ).first()

    if existing_request:
        raise HTTPException(status_code=400, detail="You Already Requested For This Book.")

    request = models.BorrowRequest(
        book_id=book_id,
        user_id = current_user_id,
        borrow_start_date=borrow_start_date,
        return_date=return_date,
        status="pending", 
    )

    db.add(request)
    db.commit()
    db.refresh(request)

    return request

def fetch_personal_history(user_id : int, db: Session):
    return db.query(models.BorrowHistory).filter(models.BorrowHistory.user_id == user_id).all()


def return_book(borrow_id: int, user_id: int, db: Session) -> schemas.BorrowHistoryResponse:
    borrow_record = db.query(models.BorrowHistory).filter(models.BorrowHistory.id == borrow_id).first()
    if not borrow_record:
        raise HTTPException(status_code=404, detail="Borrow record not found.")
    
 
    if borrow_record.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to return this book.")

  
    borrow_record.return_date = datetime.utcnow()
    borrow_record.status = "returned"
    db.commit()

   
    book = db.query(models.Book).filter(models.Book.id == borrow_record.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found.")
    
    book.available = True
    db.commit()

  
    return schemas.BorrowHistoryResponse(
        book_id=borrow_record.book_id,
        book_title=book.title,
        borrow_date=borrow_record.borrow_date,
        return_date=borrow_record.return_date,
        status=borrow_record.status
    )