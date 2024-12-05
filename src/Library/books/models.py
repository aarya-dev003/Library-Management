from sqlmodel import SQLModel, Field, Relationship
from datetime import date

class Book(SQLModel, table = True):
    __tablename__ = "book"
    id : int = Field(primary_key= True)
    title : str = Field ( nullable=False)
    author : str = Field ( nullable=False)
    available : bool =  Field (default= True, nullable=False)


class BorrowRequest(SQLModel, table = True):
    __tablename__ = "borrow_request"
    id : int = Field(primary_key=True)
    book_id : int  = Field(foreign_key="book.id", nullable=False)
    user_id : int = Field(foreign_key="user.id", nullable=False)
    borrow_start_date : date = Field ( nullable=False)
    return_date : date = Field ( nullable=False)
    status : str = Field(default="pending")

class BorrowHistroy(SQLModel, table = True):
    __tablename__ = "borrow_history"
    id : int = Field(primary_key=True)
    book_id : int = Field(foreign_key= "book.id", nullable=False)
    user_id : int = Field(foreign_key="user.id", nullable=False)
    borrow_date : date = Field ( nullable=False)
    return_date : date = Field ( nullable=False)