
# from starlette.status import HTTP_201_CREATED
from app.oauth2 import get_current_user
from ..masterImports import * 
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi import status
from app import schemas, database, models, oauth2

router = APIRouter(tags=['vote'])


@router.get("/votes")
def get_votes(db:Session=Depends(get_db)):
    all_votes = db.query(models.VotesTable).all()
    return all_votes

@router.post("/votes/{id}")
def cast_vote(id:int, db:Session=Depends(get_db)):
    loggedinUser_id = (db.query(models.loginsTable.owner_id).all())[-1][0]    
    print(f'loggedinUser_id: {loggedinUser_id}')

    new_vote = models.VotesTable(voter_id=loggedinUser_id, post_id=id)

    mypost = db.query(models.sqlaPost).filter(models.sqlaPost.id==id).all()

    if mypost != []:
        print(f'mypost: {mypost}')
        print(f'mypost: {mypost[0].id}')
        
    # print(f'str(new_vote): {str(new_vote)}')
    # post_exists = (db.query(str(models.sqlaPost.id)==str(id)).first())[0]
    
    # print(f'post_exists: {post_exists}')

    no_votes = db.query(models.VotesTable).filter(models.VotesTable.voter_id==loggedinUser_id, models.VotesTable.post_id==id).all()

    # return len(no_votes)==0
    
    if not mypost: # if mypost == []
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f'ERROR: A post with id:{id} does not exist')

    if len(no_votes) != 0:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'ERROR: User_id:{loggedinUser_id} has already voted for post_id:{id}')
    # DETAIL:  Key (user_id, post_id)=(31, 22) already exists.

    db.add(new_vote)
    db.commit()
    db.refresh(new_vote)

    return new_vote


@router.post("/vote", status_code=status.HTTP_201_CREATED)
def new_vote(vote: schemas.CastVote_schema, db:Session=Depends(get_db), current_user:int=Depends(oauth2.get_current_user)):

    post_query = db.query(models.sqlaPost).filter(models.sqlaPost.id==vote.post_id)
    found_post = post_query.first()
    
    vote_query = db.query(models.VotesTable).filter(models.VotesTable.post_id==vote.post_id, models.VotesTable.voter_id==current_user.id)
    found_vote = vote_query.first()

    print(f'current_user: {current_user.id}')

    existing_vote = db.query(models.VotesTable).filter(models.VotesTable.post_id==vote.post_id, models.VotesTable.voter_id==current_user.id).first()

    # return vote_query.first()
    
    if not found_post:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f'ERROR: A post with id:{vote.post_id} does not exist')

    if found_post:
        if vote.vote_dir==1:
            if not found_vote:
                new_vote = models.VotesTable(post_id=vote.post_id, voter_id=current_user.id, vote_type=vote.vote_dir)
                db.add(new_vote)
                db.commit()
                return{'SUCCESSFULLY ADDED VOTE' : {'voter_id':current_user.id, 'post_id':vote.post_id, 'vote':vote.vote_dir}}
            if found_vote and existing_vote.vote_type==1:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'ERROR: User_id:{current_user.id} has already voted: {vote.vote_dir} for post_id:{vote.post_id}')
            else:
                vote_query.update({"post_id":vote.post_id, "voter_id":current_user.id, "vote_type":vote.vote_dir}, synchronize_session=False)
                db.commit()
                # return {'SUCCESS': vote_query.first()}
                return{'SUCCESSFULLY UPDATED VOTE' : {'voter_id':current_user.id, 'post_id':vote.post_id, 'vote':vote.vote_dir}}

        if vote.vote_dir==0:
            if not found_vote:
                raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f'CANNOT REMOVE VOTE: User_id:{current_user.id} has not yet voted for post_id:{vote.post_id}')
            else:
                vote_query.delete(synchronize_session=False)
                db.commit()
                return{'SUCCESSFULLY REMOVED VOTE' : {'voter_id':current_user.id, 'post_id':vote.post_id, 'vote':vote.vote_dir}}

        if vote.vote_dir==-1:
            if not found_vote:
                new_vote = models.VotesTable(post_id=vote.post_id, voter_id=current_user.id, vote_type=vote.vote_dir)
                db.add(new_vote)
                db.commit()
                return{'SUCCESSFULLY ADDED VOTE' : {'voter_id':current_user.id, 'post_id':vote.post_id, 'vote':vote.vote_dir}}
            if found_vote and existing_vote.vote_type==-1:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'ERROR: User_id:{current_user.id} has already voted: {vote.vote_dir} for post_id:{vote.post_id}')
            else:
                vote_query.update({"post_id":vote.post_id, "voter_id":current_user.id, "vote_type":vote.vote_dir}, synchronize_session=False)
                db.commit()
                # return {'SUCCESS': vote_query.first()}
                return{'SUCCESSFULLY UPDATED VOTE' : {'voter_id':current_user.id, 'post_id':vote.post_id, 'vote':vote.vote_dir}}