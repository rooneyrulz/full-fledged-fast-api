from fastapi import status
from models import models


def get(response, db):
    blogs = db.query(models.Blog).all()
    if not blogs:
        response.status_code = status.HTTP_404_NOT_FOUND
        return []
    return blogs



def create(request, db):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog




def retrieve(id, response, db):
    blog = db.query(models.Blog).get(id)
    if not blog:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {}
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={})
    return blog



def update(id, request, response, db):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        response.status_code = status.HTTP_404_NOT_FOUND
        return "Blog not found!"
    blog.update({'title': request.title, 'body': request.body})
    db.commit()
    return 'Blog updated!'




def delete(id, response, db):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        response.status_code = status.HTTP_404_NOT_FOUND
        return "Blog not found!"
    blog.delete()
    db.commit()
    response.status_code = status.HTTP_200_OK
    return "Blog deleted!"