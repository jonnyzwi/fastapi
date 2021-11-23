
from app.oauth2 import get_current_user
from ..masterImports import * 
from sqlalchemy import func

router = APIRouter(tags=['sqlalchemy'])



@router.get("/sqlalchemy_join/{id}", response_model=schemas.PostOut)
def get_sqlalchemy(id:int, db: Session = Depends(get_db), limit:int=None, skip:int=None, search:Optional[str]=''):

    super_query_by_id = db.query(models.sqlaPost, func.count(models.VotesTable.post_id).label('vote_count')).join(models.VotesTable, models.VotesTable.post_id == models.sqlaPost.id, isouter=True).group_by(models.sqlaPost.id).filter(models.sqlaPost.id==str(id)).first()     

    return super_query_by_id



@router.get("/sqlalchemy_join", response_model=List[schemas.PostOut])
def get_sqlalchemy(db: Session = Depends(get_db), limit:int=None, skip:int=None, search:Optional[str]=''):
        
    results = db.query(models.sqlaPost, func.count(models.VotesTable.post_id).label('vote_count')).join(models.VotesTable, models.VotesTable.post_id==models.sqlaPost.id, isouter=True).group_by(models.sqlaPost.id)
    
    results_all = results.all()

    super_query = db.query(models.sqlaPost, func.count(models.VotesTable.post_id).label('vote_count')).join(models.VotesTable, models.VotesTable.post_id == models.sqlaPost.id, isouter=True).group_by(models.sqlaPost.id).filter(models.sqlaPost.title.contains(search)).limit(limit).offset(skip).all()
    
    # Print the raw SQL query
    print(results)
    print('\n')
    print(results_all[0])
 
 
    # return results_all
    return super_query








@router.get("/sqlalchemy", response_model=List[schemas.PostResponse])
def get_sqlalchemy(db: Session = Depends(get_db), limit:int=None, skip:int=None, search:Optional[str]=''):
    # {{URL}}sqlalchemy?limit=4&skip=3&search=
    # SQLA_posts = db.query(models.sqlaPost).all()
    SQLA_posts = db.query(models.sqlaPost).filter(models.sqlaPost.title.contains(search)).limit(limit).offset(skip).all() 
    
    # return {"All Posts": SQLA_posts}
    return SQLA_posts     # UNCOMMENT IF USING response_model



@router.get("/sqlalchemy/{id}", response_model=schemas.PostResponse)
def get_sqlalchemy(id: int, db: Session = Depends(get_db)):
    SQLA_post_by_id = db.query(models.sqlaPost).filter(models.sqlaPost.id == str(id)).first()

    if SQLA_post_by_id == None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f'ERROR: No Results with id:{str(id)}')
    else:
        # return {f'Post with id:{id}': SQLA_post_by_id}
        return SQLA_post_by_id



@router.post("/sqlalchemy", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def createSQLA(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # new_post = models.Post(title=post.title,content=post.content,published=post.published)    # CORRECT BUT INEFFICIENT # use the following to unpack dictionary models.sqlaPost(**post_dict)
    print(post.dict())
    print(f'current_user.email:{current_user.email}')
     
    # next three lines as single line
    new_post = models.sqlaPost(owner_id=current_user.id, **post.dict())
        # post_dict = post.dict()
        # post_dict['owner_id'] = current_user.id
        # new_post = models.sqlaPost(**post_dict)
    print(str(new_post))
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post #{'Newly Inserted Post': new_post}  # returning an explicit dictionary no long works after specifying response_model



@router.delete("/sqlalchemy/{id}")
def get_sqlalchemy(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    SQLA_post = db.query(models.sqlaPost).filter(models.sqlaPost.id == str(id))

    SQLA_first = SQLA_post.first()
    
    if SQLA_first == None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f'ERROR: No Results with id:{str(id)}')
    
    if current_user.id != SQLA_first.owner_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'ERROR: Post selected for deletion (post_id:{id}) was created by someone else (owner_id: {SQLA_first.owner_id}). You may only delete posts you created (your_id:{current_user.id})')

    else:
        print(f' current_user:{current_user} \n post_id:{id} \n current_user.id:{current_user.id}  \n owner.id:{SQLA_first.owner_id} \n')
        SQLA_post.delete(synchronize_session='fetch')
        db.commit()
        return {"Deleted Post": SQLA_first}



@router.put("/sqlalchemy/{id}")
def get_sqlalchemy(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    SQLA_query = db.query(models.sqlaPost).filter(models.sqlaPost.id == str(id))

    SQLA_first = SQLA_query.first()
    print(f' current_user:{current_user} \n post_id:{id} \n current_user.id:{current_user.id}  \n owner.id:{SQLA_first.owner_id} \n')
    
    if SQLA_first == None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f'ERROR: No Results with id:{str(id)}')

    if current_user.id != SQLA_first.owner_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
            detail=f'ERROR: Post selected for updating (post_id:{id}) was created by someone else (owner_id: {SQLA_first.owner_id}). You may only edit posts you created (your_id:{current_user.id})')
    else:
        print(post.dict())
        SQLA_query.update(post.dict(), synchronize_session=False)       
        db.commit()
        # db.refresh(SQLA_first)        # Not needed if return statement uses .first() on original query
        return {"Updated Post": SQLA_query.first()}



@router.get("/sqlalchemy_myposts")
def get_sqlalchemy(db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    my_posts = db.query(models.sqlaPost).filter(models.sqlaPost.owner_id == current_user.id).all()
    if not my_posts:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f'You currently have no posts (your_id:{current_user.id})')
    else:
        return {f'user_email:{current_user.email}, user_id:{current_user.id}' : my_posts}
    








# CREATE USER-DEFINED QUERY
@router.get("/sqlalchemyQuery", status_code=status.HTTP_201_CREATED)
def createSQLA(userQuery: Query, db: Session = Depends(get_db)):

    userQuery_dict = userQuery.dict()

    userQuery = str(
                userQuery_dict['columns'] + ' ' + 
                userQuery_dict['table']   + ' ' + 
                userQuery_dict['where']   + ' ' + 
                userQuery_dict['order_by']
    )

    # SQLA_query = models.Post(title=userQuery.title, content=userQuery.content)
    # SQLA_query = db.query(models.Query)

    

    # SQLA_query = db.query(models.sqlaPost(**post.dict()))       # The ** unpacks all of the potential fields in the dictionary have and organizes it in the proper schema syntax for models.Post()  # This allows us not to have to hardcode all schema columns 
    # SQLA_query = db.query(models.sqlaPost(userQuery))

    # SQLA_query = db.query(literal_column('SELECT * FROM sqlalchemy_posts'))
    # sql_query = sqlalchemy.text("SELECT * FROM sqlalchemy_posts ")
    
    # new_post = models.Post(title=post.title,content=post.content,published=post.published

    sql_query = sqlalchemy.text(userQuery)

    xx = db.query(models.sqlaPost) \
        .filter(models.sqlaPost.id > 12) \
        .filter(models.sqlaPost.id < 18) \
        .all()

    return {'User Query': xx}




