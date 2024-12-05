from sqlmodel import SQLModel, Field

class User (SQLModel, table = True):
    __tablename__ = "user"
    id : int = Field(primary_key=True)
    email : str = Field(unique=True, index=True)
    hashed_password : str
    role : str = Field(default="user")

