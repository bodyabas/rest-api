from fastapi import FastAPI
from books.router import router as books_router

app = FastAPI(title="Library API with FastAPI and MongoDB")

app.include_router(books_router)
