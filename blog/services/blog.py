from .. import models, schemas
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
def get_all_blogs(db: Session):
    blobs = db.query(models.Blog).all()
    return blobs

def get_one_blog(id:int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f'{id} not found')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail':f"{id} not found"}
    return blog

def create_blog(blog_request:schemas.Blog, db: Session):
    # new_blog = models.Blog(title = blog_request.title, body = blog_request.body)
    blog_request_obj = blog_request.model_dump()
    blog_request_obj["user_id"] = 1
    new_blog = models.Blog(**blog_request_obj)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def delete_blog(id:int, db: Session):
    query=db.query(models.Blog).filter(models.Blog.id == id) # returns a query object
    if not query.first(): # returns a query instance
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{id} not found!!!')
    # deleted_blog = query.first()
    query.delete(synchronize_session=False)
    db.commit()
    # return f"deleted record is {deleted_blog}"
    return "deleted"

def update_blog(id:int, blog_request: schemas.Blog, db:Session):
    query = db.query(models.Blog).filter(models.Blog.id == id)
    if not query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{id} not found!!!')
    # updated_blog = query.first()
    query.update(blog_request.model_dump(),synchronize_session = False)
    db.commit()
    # return f"The record before update is {updated_blog}"
    return "updated"