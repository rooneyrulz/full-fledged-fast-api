from fastapi import APIRouter, status
from sqlalchemy.orm.session import Session
from starlette.responses import Response
from fastapi.params import Depends

from config.database import get_db
from models import schemas
from controllers import user

router = APIRouter(
    prefix='/api/user',
    tags=['User']
)




@router.post('/create', response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return user.create(request, db)
    



@router.get('/{id}', response_model=schemas.UserResponse, status_code=status.HTTP_200_OK)
def get_user(id:int, response: Response, db: Session = Depends(get_db)):
    return user.retrieve(id, response, db)