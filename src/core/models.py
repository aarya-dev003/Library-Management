from sqlmodel import SQLModel, Field, Relationship
from datetime import date

class User (SQLModel, table = True):
    __tablename__ = "user"
    id : int = Field(primary_key=True)
    email : str = Field(unique=True, index=True)
    hashed_password : str
    role : str = Field(default="user")
    borrow_requests: list["BorrowRequest"] = Relationship(back_populates="user")
    borrow_history: list["BorrowHistory"] = Relationship(back_populates="user")



class Book(SQLModel, table=True):
    __tablename__ = "book"
    id: int = Field(primary_key=True)
    title: str = Field(nullable=False)
    author: str = Field(nullable=False)
    available: bool = Field(default=True, nullable=False)

    borrow_requests: list["BorrowRequest"] = Relationship(back_populates="book")
    borrow_history: list["BorrowHistory"] = Relationship(back_populates="book")


class BorrowRequest(SQLModel, table=True):
    __tablename__ = "borrow_request"
    id: int = Field(primary_key=True)
    book_id: int = Field(foreign_key="book.id", nullable=False)
    user_id: int = Field(foreign_key="user.id", nullable=False)
    borrow_start_date: date = Field(nullable=False)
    return_date: date = Field(nullable=False)
    status: str = Field(default="pending")

    book: Book = Relationship(back_populates="borrow_requests")
    user: "User" = Relationship(back_populates="borrow_requests")


class BorrowHistory(SQLModel, table=True):
    __tablename__ = "borrow_history"
    id: int = Field(primary_key=True)
    book_id: int = Field(foreign_key="book.id", nullable=False)
    user_id: int = Field(foreign_key="user.id", nullable=False)
    borrow_date: date = Field(nullable=False)
    return_date: date = Field(nullable=False)

    book: Book = Relationship(back_populates="borrow_history")
    user: "User" = Relationship(back_populates="borrow_history")
