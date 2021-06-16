from fastapi import APIRouter, HTTPException, status
from sqlalchemy.orm.session import Session
from starlette.responses import Response
from fastapi.params import Depends
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm

from config.database import get_db
from models import schemas, models
from config.hash import Hash
from config import config


router = APIRouter(
    prefix='/api/auth',
    tags=['Authentication']
)


@router.post('/login', response_model=schemas.Token, status_code=status.HTTP_200_OK)
def login(response: Response, request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        response.status_code = status.HTTP_404_NOT_FOUND
        return "Invalid credentials!"
    if not Hash().verify(user.password, request.password):
        response.status_code = status.HTTP_404_NOT_FOUND
        return "Invalid credentials!"
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = config.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}




@router.get('/current-user', status_code=status.HTTP_200_OK)
def get_current_active_user(current_user: schemas.User = Depends(config.get_current_user)):
    if not current_user:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

