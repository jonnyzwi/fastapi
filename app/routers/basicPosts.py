from ..masterImports import * 
# router = APIRouter(prefix="/posts", tags=['Posts'])
router = APIRouter(tags=['SimplePosts'])




# Decorator converts the function into one specifically tied to FastAPI
# Specifically here, it assigns an HTTP method GET
# Allows the API to get the URL after the / path as the root path (for example router.get("/login"))
@router.get("/")
def getRootPath():
    return {"message": "ooooo"}




@router.get("/posts")
def getPosts():
    # return {"data": "This is a post you just got"}
    return {"All Posts in my_posts": my_posts}


        # @router.post("/createpost")
        # def createPost(payLoad: dict= Body(...)):
        #     print(payLoad)
        #     # return {"message": "Succesfully created post"}
        #     return {"new_post": f"TITLE: {payLoad['title']} CONTENT: {payLoad['content']}" }



@router.get("/posts/{id}")
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
   

@router.get("/posts/latest")
def getLatestPost():
    latestPost = my_posts[-1]
    return {"latestPost": latestPost}    


@router.post("/posts", status_code=status.HTTP_201_CREATED)
def createPosts(new_post: schemas.SimplePost, id=0):
    print(f'new_post (complete): {new_post}')
    print(f'new_post.title: {new_post.title}')
    print(f'new_post.content: {new_post.content}')
    print(f'new_post.published: {new_post.published}')
    print(f'new_post.rating: {new_post.rating}')
    print(f'new_post.dict(): {new_post.dict()}')

    post_dict = new_post.dict()

    post_dict['id'] = randrange(0,10000000) if id==str(0) else id
    my_posts.append(post_dict)


    # return {"message": "Succesfully created post"}
    # return {"data": "returned result of schema-enforced POST request"}
    # return {"data": new_post}
    return {"data": post_dict}
    


def get_index(id):
    for i,post in enumerate(my_posts):
        if post['id'] == int(id):
            return (i,post)


@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletePost(id: int):

    if get_index(id) == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id:{id} does not exist')
    else:
        index = get_index(id)[0]
        fullPost  = get_index(id)[1]

        my_posts.pop(index)
        return {'Delete Request': f'Deleted post: {fullPost}'}


@router.put("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
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

