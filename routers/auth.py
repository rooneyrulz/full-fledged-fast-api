from fastapi import APIRouter, status
from sqlalchemy.orm.session import Session
from starlette.responses import Response
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm

from config.database import get_db
from models import schemas
from config import config
from controllers import auth

router = APIRouter(
    prefix='/api/auth',
    tags=['Authentication']
)


@router.post('/login', response_model=schemas.Token, status_code=status.HTTP_200_OK)
def login(response: Response, request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return auth.authenticate(response, request, db)


@router.get('/current-user', status_code=status.HTTP_200_OK)
def get_current_active_user(current_user: schemas.User = Depends(config.get_current_user)):
    return auth.get_authenticated_user(current_user)
