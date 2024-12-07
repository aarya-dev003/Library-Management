from sqladmin import Admin, ModelView
from src.core.models import User, BorrowRequest, BorrowHistory, Book
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from src.utils.rbac import verify_librarian
from src.core.config import settings
from src.core.security import hash_password
from src.library.books.services import process_requests
from wtforms import SelectField
from src.library.books import schemas




oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/admin/login")

class UserAdmin(ModelView, model = User):
    column_list = [User.id, User.email]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    
    
    def is_accessible(self, request):
        return Depends(verify_librarian)
    
    def on_model_change(self, data, model, is_created, request):

        if 'hashed_password' in data:  
            data['hashed_password'] = hash_password(data['hashed_password'])  
        return super().on_model_change(data, model, is_created, request)
    
class BorrowRequestAdmin(ModelView, model=BorrowRequest):
    column_list = [BorrowRequest.id, BorrowRequest.book_id, BorrowRequest.user_id, BorrowRequest.borrow_start_date, BorrowRequest.return_date, BorrowRequest.status]
    form_columns = [BorrowRequest.book_id, BorrowRequest.user_id, BorrowRequest.borrow_start_date, BorrowRequest.return_date, BorrowRequest.status]

    form_args = {
        'status': {
            'choices': [
                ('pending', 'Pending'),
                ('approved', 'Approved'),
                ('rejected', 'Rejected')
            ],
            'coerce': str,
            'label': 'Status'
        }
    }

    # Override the status field with SelectField
    form_overrides = {
        'status': SelectField
    }


    def is_accessible(self, request):
        return Depends(verify_librarian)

    # def on_model_change(self, data, model, is_created, request):
    #     if not is_created:  
    #         if model.status in ["approved", "rejected"]:
    #             # print(data['status'], model.id)
    #             # process_requests(model.id, action= schemas.BorrowApproved(action= data['status']), db = request.session )
            
    #     return super().on_model_change(data, model, is_created, request)






class BorrowHistroyAdmin(ModelView, model=BorrowHistory):
    column_list = [BorrowHistory.id, BorrowHistory.book_id, BorrowHistory.user_id, BorrowHistory.borrow_date, BorrowHistory.return_date]
    form_columns = [BorrowHistory.book_id, BorrowHistory.user_id, BorrowHistory.borrow_date, BorrowHistory.return_date]
    
    def is_accessible(self, request):
        return Depends(verify_librarian)
    

class BookAdmin(ModelView, model=Book):
    column_list = ['id', 'title', 'author', 'available']
    form_columns = ['title', 'author', 'available']
    column_searchable_list = ['title', 'author']
