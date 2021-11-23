
from ..masterImports import * 
router = APIRouter(tags=['Postgres'])


# FOR CONNECTING TO POSTGRES VIA CURSOR()
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


def get_index(id):
    for i,post in enumerate(my_posts):
        if post['id'] == int(id):
            return (i,post)


@router.get('/postgres')
def getPostgres():
    cursor.execute('''SELECT * FROM posts''')
    posts = cursor.fetchall()
    return {'data': posts}


@router.post("/postgres", status_code=status.HTTP_201_CREATED)
def createPostgres(pgPost: schemas.PostCreate):
    cursor.execute( 
        """INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """, 
        (pgPost.title, pgPost.content,pgPost.published) 
    )
    new_post = cursor.fetchone()
    conn.commit()
    return {'Newly Inserted Post': new_post}


@router.get("/postgres/{id}")
def getPostgres(id: int):
    print(f'\nGET Postgres by id: {id}')
    
    cursor.execute('''SELECT * FROM posts WHERE id = %s''',(str(id)))
    
    result = cursor.fetchone()

    if result == None:
        return {'ERROR': f'Post with id:{id} does not exist'}
    else:
        return {'query': result}


@router.get("/postgresQuery")
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


@router.delete("/postgres/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletePost(id: int):
    cursor.execute('''DELETE FROM posts WHERE id = %s RETURNING * ''', (str(id),))

    result = cursor.fetchone()

    conn.commit()

    if result == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id:{id} does not exist')
    else:
        return {'Delete Request': result}


@router.put("/postgres/{id}", status_code=status.HTTP_204_NO_CONTENT)
def updatePost(id: int, post: schemas.PostCreate):
    try:
        cursor.execute('''UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING * ''', (post.title, post.content, post.published, str(id)) )
        conn.commit()
        check_query = cursor.execute('''SELECT * FROM posts WHERE id =%s ''', (str(id)) )
        result = cursor.fetchone()
        print(f'result: {result}')

        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'ERROR: Post with id:{str(id)} does not exist')
        return {f'Updated Post for ID:{id}' : result}
    except:
        TypeError
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'ERROR: Post with id:{str(id)} does not exist')


