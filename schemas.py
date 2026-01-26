from pydantic import BaseModel, ConfigDict, Field, EmailStr
from datetime import datetime


class UserBase(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    email: EmailStr = Field(max_length=120)
    
    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int 
    image_file: str | None
    image_path: str
    
    
class UserUpdate(BaseModel):
    username: str | None = Field(default=None, min_length=1, max_length=50)
    email: EmailStr | None = Field(default=None, max_length=120)
    image_file: str | None = Field(default=None, min_length=1, max_length=200)


class PostBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    content: str = Field(min_length=1)
    published: bool = False

    model_config = ConfigDict(from_attributes=True)

class PostCreate(PostBase):
    user_id: int # Temporary, to link post to a user
    
class PostUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    content: str | None = Field(default=None, min_length=1)
    published: bool | None = None


class PostResponse(PostBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user_id: int
    date_posted: datetime
    author: UserResponse
