from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from .. import models, database
from ..security import verify_password
from datetime import timedelta
from ..JWTtoken import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(tags=["Login"])

@router.post("/login", status_code=status.HTTP_200_OK)
def login_user(login_request:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == login_request.username).first()
    if not user or not verify_password(login_request.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials!!!")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
