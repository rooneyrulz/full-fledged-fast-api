from fastapi import status
from models import models
from config.hash import Hash

def create(request, db):
    new_user = models.User(name=request.name, email=request.email, password=Hash().bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



def retrieve(id, response, db):
    user = db.query(models.User).get(id)
    if not user:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {}
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={})
    return user
