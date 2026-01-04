from .. import schemas, models
from sqlalchemy.orm import Session
from fastapi import HTTPException,status
from ..security import hash_password
def create_user(user_request:schemas.User, db:Session):
    user_data = user_request.model_dump()
    user_data["password"] = hash_password(user_request.password)
    # print(user_data["password"])
    new_user = models.User(**user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_by_id(id:int, db:Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f'{id} not found')
    return user
