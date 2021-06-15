from fastapi import APIRouter, status
from sqlalchemy.orm.session import Session
from starlette.responses import Response
from fastapi.params import Depends

from config.database import get_db
from config.hash import Hash
from models import schemas, models

router = APIRouter(
    prefix='/api/user',
    tags=['User']
)




@router.post('/create', response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name=request.name, email=request.email, password=Hash().bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



@router.get('/{id}', response_model=schemas.UserResponse, status_code=status.HTTP_200_OK)
def get_user(id:int, response: Response, db: Session = Depends(get_db)):
    user = db.query(models.User).get(id)
    if not user:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {}
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={})
    return user