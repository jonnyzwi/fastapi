
from ..masterImports import * 

router = APIRouter(tags=['userTable'])

@router.get("/users", response_model=List[schemas.FullUsersResponse])
def getUser(db:Session = Depends(get_db)):
    # return {'All Users': db.query(models.usersTable).all()}
    return db.query(models.usersTable).all()


@router.get("/users/{id}", response_model=newUserResponse)
def getUser(id:int, db:Session = Depends(get_db)):
    
    user_by_id = db.query(models.usersTable).filter(models.usersTable.id == str(id)).first()

    if not user_by_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'ERROR: No user with id:{str(id)}')
    else:
        return user_by_id



@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=newUserResponse)
def createUser(user: schemas.NewUser, db: Session = Depends(get_db)):

    # print(f'user: {user}')
    # print(f'user.password: {user.password}')

    #  HASH THE PASSWORD, STORED IN user.password
    hashed_pwd = utils.hash(user.password)
    user.password = hashed_pwd
    # print(user.password)

    requestedEmail = user.dict()['email']
    checkUser = db.query(models.usersTable).filter(models.usersTable.email == requestedEmail).first()

    if checkUser != None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
        detail=f'ERROR: the email address {str(requestedEmail)} is not avaialable')


    print(user.dict())
    new_user = models.usersTable(**user.dict())
    # print(str(new_user))      # <app.models.usersTable object at 0x1066d06a0>
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # return {'New User Created': new_user}
    return new_user


