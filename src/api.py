from fastapi import FastAPI
from src.auth.routes import router as auth_router

app = FastAPI(
    title= "Library Management"
)

@app.get('/')
async def home():
    return {"message": "Library Management By Aarya"}

app.include_router(auth_router, tags=['Authentication'], prefix='/auth')