# !!!!!
# THREE PIECES OF INFO
    # SECRET KEY
    # ALGO
    # EXPIRATION TIME
    # https://jwt.io/

from fastapi import Depends, status, HTTPException
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session 

from app import schemas, database, models
from .config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


# SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 60        #600000000

SECRET_KEY                  = settings.secret_key
ALGORITHM                   = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    print(f'expire: {expire}')
    print(f'encoded_jwt: {encoded_jwt}')

    return (encoded_jwt, expire)


def verify_access_token(token:str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: str = payload.get("user_id")

        if not id:
            raise credentials_exception
        
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    
    return token_data


def get_current_user(token:str = Depends(oauth2_scheme), db:Session=Depends(database.get_db) ):
    
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials', headers={"WWW-Authenticate":"Bearer"})
    
    token = verify_access_token(token, credentials_exception)

    user = db.query(models.usersTable).filter(models.usersTable.id==token.id).first()

    # return verify_access_token(token, credentials_exception)

    return user