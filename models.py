from pydantic import BaseModel
from bson import ObjectId

# To handle ObjectId serialization
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

class BlogPost(BaseModel):
    title: str
    content: str
    author: str

    class Config:
        arbitrary_types_allowed = True

class BlogPostInDB(BlogPost):
    id: PyObjectId

    class Config:
        json_encoders = {
            ObjectId: str
        }
