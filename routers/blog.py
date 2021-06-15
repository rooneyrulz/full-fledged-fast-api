from fastapi import APIRouter, status
from sqlalchemy.orm.session import Session
from starlette.responses import Response
from fastapi.params import Depends

from config.database import get_db
from models import schemas, models

router = APIRouter(
    prefix='/api/blog',
    tags=['Blog']
)



@router.get('/all', response_model=schemas.BlogResponse)
def get_all(response: Response, db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    if not blogs:
        response.status_code = status.HTTP_404_NOT_FOUND
        return []
    return blogs



@router.post('/create', status_code=status.HTTP_201_CREATED)
def create(blog: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=blog.title, body=blog.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog




@router.get('/{id}', response_model=schemas.BlogResponse)
def get_detail(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).get(id)
    if not blog:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {}
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={})
    return blog




@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_blog(id, request: schemas.Blog, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        response.status_code = status.HTTP_404_NOT_FOUND
        return "Blog not found!"
    blog.update({'title': request.title, 'body': request.body})
    db.commit()
    return 'Blog updated!'




@router.delete('/{id}')
def delete_blog(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        response.status_code = status.HTTP_404_NOT_FOUND
        return "Blog not found!"
    blog.delete()
    db.commit()
    
    response.status_code = status.HTTP_200_OK
    return "Blog deleted!"