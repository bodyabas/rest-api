from pydantic import BaseModel, constr

class BookCreate(BaseModel):
    title: constr(min_length=2, max_length=100)
    author: constr(min_length=2, max_length=50)
