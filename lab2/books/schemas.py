from pydantic import BaseModel, Field, validator

class BookSchema(BaseModel):
    title: str = Field(..., min_length=2, max_length=100)
    author: str = Field(..., min_length=2, max_length=50)

    @validator("title")
    def validate_title(cls, value):
        if not value.strip():
            raise ValueError("Title cannot be empty.")
        return value
    
    @validator("author")
    def validate_author(cls, value):
        if not value.strip():
            raise ValueError("Author cannot be empty.")
        return value
