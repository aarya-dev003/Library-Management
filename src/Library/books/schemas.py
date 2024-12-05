from pydantic import BaseModel, EmailStr, Field

class BorrowRequest(BaseModel):
    book_id : str
    start_date: str
    end_date : str
    
     