from fastapi import FastAPI, Depends, status, Response, HTTPException
# from schemas import Blog
from blog.database import engine, get_db
from blog import schemas, models
from sqlalchemy.orm import Session
from typing import List
from passlib.context import CryptContext
import hashlib
from .routers import blog, user, login
app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

app.include_router(login.router)
app.include_router(user.router)
app.include_router(blog.router)

# @app.get("/blog", status_code=status.HTTP_200_OK, response_model=List[schemas.ShowBlog], tags=['blogs'])
# def get_all_blogs(db:Session = Depends(get_db)):
#     blobs = db.query(models.Blog).all()
#     return blobs

# @app.get("/blog/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog, tags=['blogs'])
# def get_one_blog(id, response:Response, db: Session = Depends(get_db)):
#     blog = db.query(models.Blog).filter(models.Blog.id == id).first()
#     if not blog:
#         raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f'{id} not found')
#         # response.status_code = status.HTTP_404_NOT_FOUND
#         # return {'detail':f"{id} not found"}
#     return blog

# @app.post("/blog", status_code=status.HTTP_201_CREATED, response_model=schemas.ShowBlog, tags=['blogs'])
# def create_blog(blog_request:schemas.Blog, db: Session = Depends(get_db)):
#     # new_blog = models.Blog(title = blog_request.title, body = blog_request.body)
#     blog_request_obj = blog_request.model_dump()
#     blog_request_obj["user_id"] = 1
#     new_blog = models.Blog(**blog_request_obj)
#     db.add(new_blog)
#     db.commit()
#     db.refresh(new_blog)
#     return new_blog

# @app.delete("/blog/{id}", status_code=status.HTTP_201_CREATED, tags=['blogs'])
# def delete_blog(id, db: Session = Depends(get_db)):
#     query=db.query(models.Blog).filter(models.Blog.id == id) # returns a query object
#     if not query.first(): # returns a query instance
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{id} not found!!!')
#     # deleted_blog = query.first()
#     query.delete(synchronize_session=False)
#     db.commit()
#     # return f"deleted record is {deleted_blog}"
#     return "deleted"

# @app.put("/blog/{id}",status_code=status.HTTP_201_CREATED, tags=['blogs'])
# def update_blog(id, blog_request: schemas.Blog, db:Session = Depends(get_db)):
#     query = db.query(models.Blog).filter(models.Blog.id == id)
#     if not query.first():
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{id} not found!!!')
#     # updated_blog = query.first()
#     query.update(blog_request.model_dump(),synchronize_session = False)
#     db.commit()
#     # return f"The record before update is {updated_blog}"
#     return "updated"

# pass_context = CryptContext(schemes=["argon2"],deprecated="auto") # bcrypt allows only 72 bytes long (argon2_cffi)

# @app.post("/user", status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser, tags=['users'])
# def create_user(user_request:schemas.User, db:Session = Depends(get_db)):
#     user_data = user_request.model_dump()
#     sha256_hash = hashlib.sha256(user_request.password.encode("utf-8")).hexdigest()
#     user_data["password"] = pass_context.hash(sha256_hash)
#     # print(user_data["password"])
#     new_user = models.User(**user_data)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user

# @app.get("/user/{id}", response_model=schemas.ShowUser, tags=['users'])
# def get_user_by_id(id:int, db:Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.id == id).first()
#     if not user:
#         raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f'{id} not found')
#     return user
