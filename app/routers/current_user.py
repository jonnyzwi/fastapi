
from app.oauth2 import get_current_user
from ..masterImports import * 
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi import status
from app import schemas, database, models, oauth2

router = APIRouter(tags=['current_user'])

@router.get('/current_user')
def getCurrentUser(db:Session=Depends(get_db), current_user:int=Depends(oauth2.get_current_user)):
    return {'current_user.id': current_user.id, 'current_user.name': current_user.name, 'current_user.email': current_user.email}

