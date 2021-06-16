from datetime import timedelta
from fastapi import HTTPException, status

from models import models
from config.hash import Hash
from config import config


def authenticate(response, request, db):
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


def get_authenticated_user(current_user):
    if not current_user:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
