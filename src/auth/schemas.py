from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    email: EmailStr
    password : str = Field(min_length= 8 , max_length= 20)

    class Config:
        # orm_mode = True
        from_attributes = True

class UserLogin(BaseModel):
    email : EmailStr
    password : str

    class Config:
        # orm_mode = True
        from_attributes = True


class UserResponse(BaseModel):
    email : str
    id : int
    role : str
    class Config:
        # orm_mode = True
        from_attributes = True


class TokenData(BaseModel):
    token_type : str = "bearer",
    access_token : str

