
from logging import raiseExceptions
from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app import database, schemas, models, utils, oauth2

def utc_to_local(utc_datetime):
    return utc_datetime.replace(tzinfo=timezone.utc).astimezone(tz=None)

time_format = '%H:%M:%S • %Y-%m-%d'


router = APIRouter(tags=['Authentication'])

exportUser = None


@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm=Depends(), db:Session=Depends(database.get_db)):    
    # user_credentials: OAuth2PasswordRequestForm=Depends() will return dict with two elements (which were provided by user in Postman)
        # {username, password}
    user = db.query(models.usersTable).filter(models.usersTable.email == user_credentials.username).first()

    print(f'user: {user}')
    
    if user != None:
        verified = utils.verify(user_credentials.password, user.password)
        
        # print(user)
        print(f'user.id: {user.id}')
        print(f'user.email: {user.email}')
        print(f'user.password: {user.password}')
    

    if not user:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f'ERROR: No user found with email address: {user_credentials.username}') 
    
    if not verified:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail=f'ERROR: Incorrect password for email address: {user_credentials.username}')    
    
    my_tuple = oauth2.create_access_token(data={"user_id": user.id})

    access_token = my_tuple[0]

    token_expiration = utc_to_local(my_tuple[1]).strftime(time_format)

    # print(datetime.now())
    # print(type(datetime.now()))

    ##############################################################################################################
    user_attributes = [user.id, user.email, user.password]
    addLogin = models.loginsTable(owner_id=user.id, owner_email=user.email)
    db.add(addLogin)
    db.commit()
    ##############################################################################################################

    return {"access_token":access_token, "token_type":"bearer", "token_expiration": token_expiration }






# def login(user_credentials:schemas.UserLogin, db:Session=Depends(database.get_db)):
#     # hashed_password = utils.hash(user_credentials.password)
    
#     user = db.query(models.usersTable).filter(models.usersTable.email == user_credentials.email).first()
    
#     stored_pwd   = db.query(models.usersTable.password).filter(models.usersTable.email == user_credentials.email).first()
    
#     verified = utils.verify(user_credentials.password, stored_pwd[0])

#     if not user:
#         raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f'ERROR: No user foudn with email address: {user_credentials.email}') 
#     if not verified:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail=f'ERROR: Incorrect passwrod for email address: {user_credentials.email}')    
    
#     access_token = oauth2.create_access_token(data={"user_id": user.id})

#     return {"access_token": access_token, "token_type":"bearer"}

#     # else:
#     #     return f'Successful login for user {user_credentials.email}'


