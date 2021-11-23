
'''

database
    # Dependency
    def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()


oauth2
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

    def create_access_token(data: dict):
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def verify_access_token(token:str, credentials_exception):
        token_data = schemas.TokenData(id=id)
        return token_data       #as an id:int

    def get_current_user(token:str = Depends(oauth2_scheme), db:Session=Depends(database.get_db)):
        token = verify_access_token(token, credentials_exception)
        user = db.query(models.usersTable).filter(models.usersTable.id==token.id).first()
        return user         #as an id:int



auth
    @router.post('/login', response_model=schemas.Token)
        def login(user_credentials: OAuth2PasswordRequestForm=Depends(), db:Session=Depends(database.get_db)):    
            user = db.query(models.usersTable).filter(models.usersTable.email == user_credentials.username).first()
            verified = utils.verify(user_credentials.password, user.password)
            my_tuple = oauth2.create_access_token(data={"user_id": user.id})
            return {"access_token":access_token, "token_type":"bearer", "token_expiration": token_expiration }


sqlalchemy
    @router.post("/sqlalchemy", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
        def createSQLA(
            post: schemas.PostCreate, 
            db: Session = Depends(get_db), 
            current_user: int = Depends(oauth2.get_current_user)
        ):


Postman
    POST • http//:127.0.0.1:8000/sqlalchemy

        user-provided fields:
        {
            "title": "Inserted SQLAlchemy post",
            "content": "SQLAlchemy added post",
            "published": true
        }

'''