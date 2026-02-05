from pydantic import BaseModel
from datetime import datetime
from pydantic import BaseModel, EmailStr


class PostBase(BaseModel):
    title: str
    content: str
    published: bool=True
    
class CreatePost(PostBase):
    pass

class UpdatePost(PostBase):
    pass

class ResponsePost(PostBase):
    created_at:datetime
    class Config:
        from_attributes=True
        
class CreateUser(BaseModel):
    email: EmailStr
    password: str
    
class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
    class Config:
        from_attributes=True

class UserLogin(BaseModel):
    email:EmailStr
    password: str
