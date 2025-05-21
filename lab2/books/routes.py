from fastapi import APIRouter, HTTPException
from typing import List
from .schemas import BookSchema
from .storage import books
from .models import Book

router = APIRouter()

@router.get("/", response_model=List[Book])
async def get_books():
    return books

@router.get("/{book_id}", response_model=Book)
async def get_book(book_id: int):
    book = next((b for b in books if b.id == book_id), None)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/", response_model=Book, status_code=201)
async def add_book(book_schema: BookSchema):
    existing_ids = [b.id for b in books]
    new_id = 1
    while new_id in existing_ids:
        new_id += 1
    new_book = Book(id=new_id, **book_schema.dict())
    books.append(new_book)
    return new_book

@router.delete("/{book_id}", status_code=204)
async def delete_book(book_id: int):
    global books
    if not any(b.id == book_id for b in books):
        raise HTTPException(status_code=404, detail="Book not found")
    books = [b for b in books if b.id != book_id]
