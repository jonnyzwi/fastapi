
# PYDANTIC SCHEMA MODELS THAT DEFINE THE SHAPE OF REQUESTS AND RESPONSES

from pydantic import BaseModel, EmailStr
from typing import Optional
from pydantic.types import conint
from sqlalchemy.sql.sqltypes import TIMESTAMP
from datetime import datetime
from .models import sqlaPost

from app.database import Base


# SUCH A CLASS WOULD ONLY GIVE A USER ACCESS TO THE published FIELD, 
# BUT NOT ALLOW THEM TO MAKE ANY OTHER ALTERATIONS
class togglePublished(BaseModel):
    published: bool


class SimplePost(BaseModel):
    # SCHEMA: title str, content str, category str, published Bool, etc
    # When a POST request is sent, this class validates that both a title and content are provided and that they are both of type str
    title:     str
    content:   str
    published: bool=True
    rating: Optional[int]=None


class Query(BaseModel):
    columns:  str
    table:    str
    where:    Optional[str]=''
    order_by: Optional[str]=''



class PostBase(BaseModel):
    title:     str
    content:   str
    published: bool=True
    


class PostCreate(PostBase):
    # inherits all attributes and requirements of PostBase
    pass



class NewUser(BaseModel):
    name:     str
    email:    EmailStr
    password: str


class PostLogin(BaseModel):
    pass




class CastVote_schema(BaseModel):
    post_id  : int
    vote_dir: conint(ge=-1,le=1)




                                ### RESPONSES ###



class UserToPost(BaseModel):    # FROM HIS  UserOut(BaseModel):
    id:         int
    name:       str
    email:      EmailStr
    password:   str
    created_at: datetime
    
    class Config:
        orm_mode = True


class PostResponse(PostBase):  # FROM HIS   Post(PostBase):
    id:         int
    title:      str
    content:    str
    published:  bool
    created_at: datetime
    owner_id:   int
    owner:      UserToPost
    
    class Config:
        orm_mode = True




class PostOut(BaseModel):  # FROM HIS   PostOut(BaseModel):
    sqlaPost: PostResponse
    vote_count: int

    class Config:
        orm_mode = True







class FullUsersResponse(BaseModel):
    # Specify all fields that we desire in return from the fastAPI response
    id:         int
    name:       str
    email:      EmailStr
    password:   str
    created_at: datetime
    class Config:
        orm_mode = True

class newUserResponse(BaseModel):
    # Specify all fields that we desire in return from the fastAPI response
    id:         int
    name:       str
    email:      EmailStr
    created_at: datetime
    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type  : str
    token_expiration: str
    # token_expiration: datetime


class TokenData(BaseModel):
    id: Optional[str] = None


class loginResponse(BaseModel):
    owner_id: int