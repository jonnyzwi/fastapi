
from ..masterImports import * 

router = APIRouter(tags=['loginsTable'])

@router.get("/logins")#, response_model=List[schemas.FullUsersResponse])
def getUser(db:Session = Depends(get_db)):
    # return {'All Users': db.query(models.usersTable).all()}
    return db.query(models.loginsTable).all()
