from fastapi import APIRouter, status, Depends, Response
from sqlalchemy.orm import Session
from .. import database,schemas
from typing import List
from ..services import blog
from ..JWTtoken import get_current_user
from .. import schemas

router = APIRouter(prefix="/blog", tags=['Blogs'])
get_db = database.get_db

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.ShowBlog])
def get_all_blogs(db:Session = Depends(get_db), current_user: schemas.User= Depends(get_current_user)):
    return blog.get_all_blogs(db)

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def get_one_blog(id:int, response:Response, db: Session = Depends(get_db)):
    return blog.get_one_blog(id,db)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ShowBlog)
def create_blog(blog_request:schemas.Blog, db: Session = Depends(get_db)):
    return blog.create_blog(blog_request,db)

@router.delete("/{id}", status_code=status.HTTP_201_CREATED)
def delete_blog(id:int, db: Session = Depends(get_db)):
    return blog.delete_blog(id,db)

@router.put("/{id}",status_code=status.HTTP_201_CREATED)
def update_blog(id:int, blog_request: schemas.Blog, db:Session = Depends(get_db)):
    return blog.update_blog(id,blog_request,db)