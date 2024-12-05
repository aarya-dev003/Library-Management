from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    database_hostname : str = os.getenv("DATABASE_HOSTNAME" , "localhost")
    database_port : str = os.getenv("DATABASE_PORT" , "5432")
    database_password : str = os.getenv("DATABASE_PASSWORD" , "2003")
    database_name : str = os.getenv("DATABASE_NAME" , "library")
    database_username : str = os.getenv("DATABASE_USERNAME" , "postgres")
    SECRET_KEY : str  = os.getenv("SECRET_KEY" , "localhost")
    ALGORITHM : str  = os.getenv("ALGORITHM" , "HS512")
    ACCESS_TOKEN_EXPIRE_MINUTES : int = 60 

    class Config:
        env_file = ".env"

settings = Settings() 