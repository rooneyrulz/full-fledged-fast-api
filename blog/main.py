from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from sqlalchemy.orm.session import Session
from starlette.responses import Response
from starlette.status import HTTP_204_NO_CONTENT
from . import schemas, models
from .database import SessionLocal, engine


app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create(blog: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=blog.title, body=blog.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blogs')
def get_all(response: Response, db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    if not blogs:
        response.status_code = status.HTTP_404_NOT_FOUND
        return []
    return blogs
 

@app.get('/blog/{id}')
def get_detail(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).get(id)
    if not blog:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {}
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={})
    return blog



@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_blog(id, request: schemas.Blog, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        response.status_code = status.HTTP_404_NOT_FOUND
        return "Blog not found!"
    blog.update(request)
    db.commit()
    return "Blog updated!"



@app.delete('/blog/{id}')
def delete_blog(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        response.status_code = status.HTTP_404_NOT_FOUND
        return "Blog not found!"
    blog.delete()
    db.commit()
    
    response.status_code = status.HTTP_200_OK
    return "Blog deleted!"

