from pydantic import BaseModel

class PostCreate(BaseModel):
    title: str
    content: str | None = None
    class Config:
        orm_mode = True

class Post(PostCreate):
    id: int
    title: str
    content: str | None = None
    class Config:
        orm_mode = True
