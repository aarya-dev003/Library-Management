from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date,datetime


class BookResponse(BaseModel):
    id : int
    title : str
    author : str 
    available : bool

    class Config:
        from_attributes : True
     
class BorrowRequest(BaseModel):
    book_id : int
    start_date: date
    end_date : date
    user_id : int

    class Config:
        from_attributes : True


class BookCreateSchema(BaseModel):
    title: str
    author: str
    available: Optional[bool] = True 

    class Config:
        from_attributes : True


class BorrowRequestCreate(BaseModel):
    book_id: int
    borrow_start_date: date
    return_date: date

    class Config:
        from_attributes = True

class BorrowApproved(BaseModel):
    action : str

    class Config:
        from_attributes = True

class Request_Out(BaseModel):
    id: int
    book_id : int
    borrow_start_date : date
    return_date : date
    status : str
    class Config:
        from_attributes = True

from pydantic import BaseModel
from typing import Optional

class BorrowHistoryResponse(BaseModel):
    book_id: int
    book_title: str
    borrow_date: datetime
    return_date: Optional[datetime]
    status: str

    class Config:
        from_attributes = True
