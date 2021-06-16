from typing import List
from fastapi import APIRouter, status
from sqlalchemy.orm.session import Session
from starlette.responses import Response
from fastapi.params import Depends

from config.database import get_db
from models import schemas
from config import config
from controllers import blog

router = APIRouter(
    prefix='/api/blog',
    tags=['Blog']
)



@router.get('/all', response_model=List[schemas.BlogResponse])
def get_all(response: Response, db: Session = Depends(get_db), current_user: schemas.User = Depends(config.get_current_user)):
    return blog.get(response, db)



@router.post('/create', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db), current_user: schemas.User = Depends(config.get_current_user)):
    return blog.create(request, db)




@router.get('/{id}', response_model=schemas.BlogResponse)
def get_detail(id, response: Response, db: Session = Depends(get_db), current_user: schemas.User = Depends(config.get_current_user)):
    return blog.retrieve(id, response, db)




@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_blog(id, request: schemas.Blog, response: Response, db: Session = Depends(get_db), current_user: schemas.User = Depends(config.get_current_user)):
    return blog.update(id, request, response, db)




@router.delete('/{id}')
def delete_blog(id, response: Response, db: Session = Depends(get_db), current_user: schemas.User = Depends(config.get_current_user)):
    return blog.delete(id, response, db)