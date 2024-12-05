from sqlmodel import create_engine, Session
from src.core.config import settings

# SQL_ALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database-name>'
DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'


engine = create_engine(DATABASE_URL, echo=False)

def get_db():
    with Session(engine) as session:
        yield session