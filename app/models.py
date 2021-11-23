
# CREATE CLASSES THAT DEFINE THE CREATION OF TABLES IN PGADMIN 
# TABLES ARE AUTOAMTICALLY CREATED WHEN CODE IS SAVED - NO NEED TO 
# RUN A CREATE TABLE FUNCTION


from os import X_OK
from pydantic.networks import EmailStr
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import null, text
from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey
from typing import Optional


class sqlaPost(Base):
    __tablename__ = "sqlalchemy_posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=True, server_default='True')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("usersTable") #Creates a relationship with Class usersTable


class usersTable(Base):
    __tablename__ = 'users'

    id          = Column(Integer, primary_key=True, nullable=False)
    name        = Column(String , nullable=False)
    email       = Column(String , nullable=False, unique=True)
    password    = Column(String , nullable=False)
    created_at  = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class loginsTable(Base):
    __tablename__ = 'logins'

    login_number = Column(Integer, primary_key=True, nullable=False)
    login_time   = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    owner_id     = Column(Integer, ForeignKey("users.id", ondelete="CASCADE")   , nullable=False)
    owner_email  = Column(String , ForeignKey("users.email", ondelete="CASCADE"), nullable=False)





class VotesTable(Base):
    __tablename__ = 'votes'

    voter_id  = Column(Integer, ForeignKey("users.id"           , ondelete="CASCADE"), primary_key=True, nullable=False)
    post_id   = Column(Integer, ForeignKey("sqlalchemy_posts.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    vote_type = Column(Integer, nullable=False)