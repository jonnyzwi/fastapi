from logging import exception
from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

from pydantic.fields import SHAPE_DEFAULTDICT
from pydantic.typing import NoneType

import psycopg2
from psycopg2.extras import RealDictCursor

import time

from . import models, schemas, utils, oauth2
from .schemas import NewUser, SimplePost, Query, newUserResponse
from .database import Base, get_db, engine, SessionLocal
# from .utils import *
import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import null, text, literal_column



my_posts =[
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "This is the second post", "content": "blah blah blah", "id": 2},
    {"title": "This is the third post", "content": "Here we are in content 3", "id": 3}
]


def find_post(id):
    for post in my_posts:
        if post['id'] == int(id):
            print(f'post: {post}')
            return post


