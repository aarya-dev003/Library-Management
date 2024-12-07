from fastapi import FastAPI, Depends
from src.auth.routes import router as auth_router
from src.utils.rbac import verify_librarian
from src.library.books.routes import router as librarian_router
from src.library.books.user_routes import router_user as user_router
from starlette.middleware.sessions import SessionMiddleware
from src.admin.admin import UserAdmin, BorrowRequestAdmin, BorrowHistroyAdmin, BookAdmin
from src.core.database import engine
from sqladmin import Admin
from src.admin.admin_auth import AdminAuth
from .middleware import add_cors_middleware


app = FastAPI(
    title= "Library Management"
)
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")
add_cors_middleware(app)
admin = Admin(app = app , engine=engine, authentication_backend=AdminAuth(secret_key="secret"))

@app.get('/')
async def home():
    return {"message": "Library Management By Aarya"}

# @app.get('/admin', dependencies=[Depends(verify_librarian)])
# async def admin_panel():
#     admin.add_view(UserAdmin)


admin.add_view(UserAdmin)
admin.add_view(BookAdmin)
admin.add_view(BorrowHistroyAdmin)
admin.add_view(BorrowRequestAdmin)


# @app.on_event("startup")
# async def setup_admin():
#     admin.views = Depends(verify_librarian)


app.include_router(auth_router, tags=['Authentication'], prefix='/auth')
app.include_router(librarian_router, tags=['Libararian'], prefix='/librarian')
app.include_router(user_router, tags=['User'], prefix='/user')

