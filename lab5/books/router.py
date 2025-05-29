from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from bson import ObjectId

from database import books_collection
from .models import Book
from .schemas import BookCreate

router = APIRouter(prefix="/books", tags=["books"])

@router.get("/", response_model=List[Book])
async def get_books():
    cursor = books_collection.find({})
    books = []
    async for doc in cursor:
        doc['id'] = str(doc['_id'])
        books.append(Book(**doc))
    return books

@router.get("/{book_id}", response_model=Book)
async def get_book(book_id: str):
    try:
        oid = ObjectId(book_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid book ID")

    book = await books_collection.find_one({"_id": oid})
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return Book(**book)

@router.post("/", response_model=Book, status_code=201)
async def create_book(book: BookCreate):
    book_dict = book.dict()
    result = await books_collection.insert_one(book_dict)
    new_book = await books_collection.find_one({"_id": result.inserted_id})
    return Book(**new_book)

@router.delete("/{book_id}")
async def delete_book(book_id: str):
    try:
        oid = ObjectId(book_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid book ID")

    result = await books_collection.delete_one({"_id": oid})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Book not found")

    return {"message": "Book deleted successfully"}
