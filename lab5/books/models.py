from pydantic_mongo import PydanticObjectId
from pydantic import BaseModel, Field

class Book(BaseModel):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias="_id")
    title: str
    author: str

    class Config:
        allow_population_by_field_name = True
        json_encoders = {PydanticObjectId: str}
