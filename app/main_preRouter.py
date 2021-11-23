
# https://www.youtube.com/watch?v=0sOvCWFmrtA&t=5h08m30s

# RUN IN TERMINAL TO START CONNECTION BETWEEN main.py AND SERVER
        # uvicorn app.main:app --reload
# ALSO CHECK TO MAKE SURE THAT BOTH THE INTERPRETER AND THE TERMINAL SHELL ARE IN VIRTUAL ENVIRONMENT venv

from logging import exception
from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

from pydantic.fields import SHAPE_DEFAULTDICT
from pydantic.typing import NoneType

import psycopg2
from psycopg2.extras import RealDictCursor

import time

from . import models, schemas, utils
from .schemas import NewUser, Post, Query, newUserResponse
from .database import Base, get_db, engine, SessionLocal
# from .utils import *
import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import null, text, literal_column






models.Base.metadata.create_all(bind=engine)

app = FastAPI()



while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi_DB', user='postgres', password='postgres', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print(f'\n\tSUCCESSFULLY CONNECTED TO DATABASE\n')
        break
    except Exception as error:
        print(f'\n\tFailed Connecting to Database\n')
        print(f'ERROR: {error}')
        time.sleep(2)


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



# Decorator converts the function into one specifically tied to FastAPI
# Specifically here, it assigns an HTTP method GET
# Allows the API to get the URL after the / path as the root path (for example app.get("/login"))
@app.get("/")
def getRootPath():
    return {"message": "ooooo"}


@app.get("/posts/latest")
def getLatestPost():
    latestPost = my_posts[-1]
    return {"latestPost": latestPost}    




@app.get("/posts")
def getPosts():
    # return {"data": "This is a post you just got"}
    return {"data": my_posts}


        # @app.post("/createpost")
        # def createPost(payLoad: dict= Body(...)):
        #     print(payLoad)
        #     # return {"message": "Succesfully created post"}
        #     return {"new_post": f"TITLE: {payLoad['title']} CONTENT: {payLoad['content']}" }



@app.post("/posts", status_code=status.HTTP_201_CREATED)
def createPosts(new_post: schemas.PostCreate, id=0):
    print(f'new_post (complete): {new_post}')
    print(f'new_post.title: {new_post.title}')
    print(f'new_post.content: {new_post.content}')
    print(f'new_post.published: {new_post.published}')
    print(f'new_post.rating: {new_post.rating}')
    print(f'new_post.dict(): {new_post.dict()}')

    post_dict = new_post.dict()

    post_dict['id'] = randrange(0,10000000) if id==0 else id
    my_posts.append(post_dict)


    # return {"message": "Succesfully created post"}
    # return {"data": "returned result of schema-enforced POST request"}
    # return {"data": new_post}
    return {"data": post_dict}
    

@app.get("/posts/{id}")
def getPost(id: int):
    print(f'\nGET post by id: {id}')
    post = find_post(id)
        
    if post == None:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f'A post with id({id}) does not exist'
                )

    return post
    

                            # def getPost(id: int, response: Response):
                            #     print(f'GET post by id: {id}')
                            #     try:
                            #         post = find_post(id)
                            #         print(f'print(post): {post}')
                            #         # return {"data": f'You have requested post id: {id}'}
                            #         if post == None:
                            #             # response.status_code = status.HTTP_404_NOT_FOUND
                            #             # return {"Error": f'{response.status_code}: A post with id({id}) does not exist'}
                            #             raise HTTPException(
                            #                 status_code=status.HTTP_404_NOT_FOUND, 
                            #                 detail=f'A post with id({id}) does not exist'
                            #                 )
                            #         return post
                            #     except: 
                            #         ValueError
                            #         print(f'\tValueError: id must be of type int')
                            #         return f'ValueError: id must be of type int. Value provided was {id}'
   

def get_index(id):
    for i,post in enumerate(my_posts):
        if post['id'] == int(id):
            return (i,post)


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletePost(id: int):

    if get_index(id) == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id:{id} does not exist')
    else:
        index = get_index(id)[0]
        fullPost  = get_index(id)[1]

        my_posts.pop(index)
        return {'Delete Request': f'Deleted post: {fullPost}'}


@app.put("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def updatePost(id: int, post: schemas.PostCreate):
    if get_index(id) == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id:{id} does not exist')
    else:
        index = get_index(id)[0]
        fullPost  = get_index(id)[1]

        post_dict = post.dict()
        post_dict['id'] = id

        my_posts[index] = post_dict

        return {'updated Post':f'{post_dict}'}


@app.get('/postgres')
def getPostgres():
    cursor.execute('''SELECT * FROM posts''')
    posts = cursor.fetchall()
    return {'data': posts}


@app.post("/postgres", status_code=status.HTTP_201_CREATED)
def createPostgres(pgPost: schemas.PostCreate):
    cursor.execute( 
        """INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """, 
        (pgPost.title, pgPost.content,pgPost.published) 
    )
    new_post = cursor.fetchone()
    conn.commit()
    return {'Newly Inserted Post': new_post}


@app.get("/postgres/{id}")
def getPostgres(id: int):
    print(f'\nGET Postgres by id: {id}')
    
    cursor.execute('''SELECT * FROM posts WHERE id = %s''',(str(id)))
    
    result = cursor.fetchone()

    if result == None:
        return {'ERROR': f'Post with id:{id} does not exist'}
    else:
        return {'query': result}


@app.get("/postgresQuery")
def getPostgres(userQuery: schemas.Query):

    userQuery_dict = userQuery.dict()
    # print(f'userQuery: {userQuery}')
    # print(f'userQuery_dict: {userQuery_dict}')

    query = str(
                userQuery_dict['columns'] + ' ' + 
                userQuery_dict['table']   + ' ' + 
                userQuery_dict['where']   + ' ' + 
                userQuery_dict['order_by']
    )

    # print(query)

    cursor.execute(query)
    
    result = cursor.fetchall()

    if result == []:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f'ERROR: No Results for query: {query}')
        # return {'ERROR': f'No Results for query: {query}'}
    else:
        return {'Query:': result}


@app.delete("/postgres/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletePost(id: int):
    cursor.execute('''DELETE FROM posts WHERE id = %s RETURNING * ''', (str(id),))

    result = cursor.fetchone()

    conn.commit()

    if result == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id:{id} does not exist')
    else:
        return {'Delete Request': result}


@app.put("/postgres/{id}", status_code=status.HTTP_204_NO_CONTENT)
def updatePost(id: int, post: schemas.PostCreate):

    try:
        cursor.execute('''UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING * ''', (post.title, post.content, post.published, str(id)) )
        conn.commit()
        check_query = cursor.execute('''SELECT * FROM posts WHERE id =%s ''', (str(id)) )
        result = cursor.fetchone()
        print(f'result: {result}')
        return {f'Updated Post for ID:{id}' : result}
    except:
        TypeError
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'ERROR: Post with id:{str(id)} does not exist')




@app.get("/sqlalchemy")     #, response_model=List[schemas.PostResponse])
def get_sqlalchemy(db: Session = Depends(get_db)):
    SQLA_posts = db.query(models.sqlaPost).all()    
    return {"All Posts": SQLA_posts}
    # return SQLA_posts     # UNCOMMENT IF USING response_model


@app.get("/sqlalchemy/{id}")
def get_sqlalchemy(id: int, db: Session = Depends(get_db)):
    SQLA_posts = db.query(models.sqlaPost).filter(models.sqlaPost.id == str(id)).first()

    if SQLA_posts == None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f'ERROR: No Results with id:{str(id)}')
    else:
        return {f'Post with id:{id}': SQLA_posts}


@app.post("/sqlalchemy", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def createSQLA(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # new_post = models.Post(title=post.title,content=post.content,published=post.published)    # CORRECT BUT INEFFICIENT
    print(post.dict())
    new_post = models.sqlaPost(**post.dict())       # The ** unpacks all of the potential fields in the dictionary have and organizes it in the proper schema syntax for models.Post()  # This allows us not to have to hardcode all schema columns 
    print(str(new_post))
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post #{'Newly Inserted Post': new_post}  # return an explicit dictionary no long works after specifying response_model



@app.delete("/sqlalchemy/{id}")
def get_sqlalchemy(id: int, db: Session = Depends(get_db)):
    SQLA_post = db.query(models.sqlaPost).filter(models.sqlaPost.id == str(id))

    SQLA_first = SQLA_post.first()
    
    if SQLA_first == None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f'ERROR: No Results with id:{str(id)}')
    else:
        SQLA_post.delete(synchronize_session='fetch')
        db.commit()
        return {"Deleted Post": SQLA_first}





@app.put("/sqlalchemy/{id}")
def get_sqlalchemy(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    SQLA_query = db.query(models.sqlaPost).filter(models.sqlaPost.id == str(id))

    SQLA_first = SQLA_query.first()
    
    if SQLA_first == None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f'ERROR: No Results with id:{str(id)}')
    
    print(post.dict())
    SQLA_query.update(post.dict(), synchronize_session=False)       
    db.commit()
    # db.refresh(SQLA_first)        # Not needed if return statement uses .first() on original query
    return {"Updated Post": SQLA_query.first()}






# CREATE USER-DEFINED QUERY
@app.get("/sqlalchemyQuery", status_code=status.HTTP_201_CREATED)
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









@app.get("/users")
def getUser(db:Session = Depends(get_db)):
    return {'All Users': db.query(models.usersTable).all()}


@app.get("/users/{id}", response_model=newUserResponse)
def getUser(id:int, db:Session = Depends(get_db)):
    
    user_by_id = db.query(models.usersTable).filter(models.usersTable.id == str(id)).first()

    if not user_by_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'ERROR: No user with id:{str(id)}')
    else:
        return user_by_id



@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=newUserResponse)
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


