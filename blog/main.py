from fastapi import FastAPI, Depends, status, Response, HTTPException
# from schemas import Blog
from blog.database import engine, SessionLocal
from blog import schemas, models
from sqlalchemy.orm import Session
app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/blog", status_code=status.HTTP_201_CREATED)
def create_blob(blog_request:schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title = blog_request.title, body = blog_request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get("/blog", status_code=status.HTTP_200_OK)
def get_all_blogs(db:Session = Depends(get_db)):
    blobs = db.query(models.Blog).all()
    return blobs

@app.get("/blog/{id}", status_code=status.HTTP_200_OK)
def get_one_blog(id, response:Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f'{id} not found')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail':f"{id} not found"}
    return blog

@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id, db: Session = Depends(get_db)):
    deleted_blog=db.query(models.Blog).filter(models.Blog.id == id)
    if not deleted_blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{id} not found!!!')
    db.delete(synchronize_session=False)
    db.commit()
    return deleted_blog

@app.put("blog/{id}",status_code=status.HTTP_204_NO_CONTENT)
def update_blog(id, blog_request: schemas.Blog, db:Session = Depends(get_db)):
    updated_blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not updated_blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{id} not found!!!')
    db.update(blog_request,synchronize_session=False)
    db.commit()
    return updated_blog