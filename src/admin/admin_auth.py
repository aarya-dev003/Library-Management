from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from sqlmodel import Session
from starlette.middleware.sessions import SessionMiddleware
from src.core.database import get_db
from src.core.models import User
from src.auth.services import verify_password

class AdminAuth(AuthenticationBackend):
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self.middlewares = []

    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        # Query the database for user credentials
        with next(get_db()) as session:
            user = session.query(User).filter(User.email == username).first()

            if user is None:
                return False  # User not found

            # Verify password
            if not verify_password(password, user.hashed_password):
                return False  # Incorrect password

            # Check if the user is a librarian
            if user.role != "librarian":
                return False  # Not a librarian

            # Store user ID in the session
            request.session.update({"user_id": user.id})
            return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True
    
    async def authenticate(self, request: Request) -> bool:
        user_id = request.session.get("user_id")
        if not user_id:
            return False  # User not logged in

        # Optionally, check if the user is still a librarian
        with next(get_db()) as session:
            user = session.query(User).filter(User.id == user_id).first()
            if user and user.role == "librarian":
                return True

        return False

