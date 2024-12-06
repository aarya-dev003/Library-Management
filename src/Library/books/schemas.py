from pydantic import BaseModel, EmailStr, Field



class BookResponse(BaseModel):
    id : int
    title : str
    author : str 
    available : bool

    class Config:
        from_attributes : True
     
class BorrowRequest(BaseModel):
    book_id : str
    start_date: str
    end_date : str
    user_id : int
    book : BookResponse

    class Config:
        from_attributes : True