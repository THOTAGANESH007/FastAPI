from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from .. import database, schemas
from ..services import user

router = APIRouter(prefix="/user", tags=['Users'])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser)
def create_user(user_request:schemas.User, db:Session = Depends(database.get_db)):
    return user.create_user(user_request,db)

@router.get("/{id}", response_model=schemas.ShowUser)
def get_user_by_id(id:int, db:Session = Depends(database.get_db)):
    return user.get_user_by_id(id,db)