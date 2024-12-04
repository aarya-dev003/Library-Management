from fastapi import FastAPI

app = FastAPI(
    title= "Library Management"
)

@app.get('/')
async def home():
    return {"message": "Library Management By Aarya"}