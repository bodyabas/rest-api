from fastapi import FastAPI
from books.routes import router

app = FastAPI()
app.include_router(router, prefix="/books", tags=["books"])
