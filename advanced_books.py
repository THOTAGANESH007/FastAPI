from fastapi import FastAPI, Path, Query, HTTPException, Body
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from starlette import status
from datetime import date

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date

# for pydantic
class BookRequest(BaseModel):
    id: Optional[int] = Field(description = 'Id is optional', default = None)
    title: str = Field(min_length = 3)
    author: str = Field(min_length = 3)
    description: str = Field(min_length = 3, max_length = 100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gte=2004, lte=2030)

    # Add metadata to the swagger docs
    model_config = ConfigDict(
        json_schema_extra={
            "example":{
                "title":"Book Name",
                "author": "Tiger",
                "description": "Add description of a book",
                "rating": 5,
                'published_date': 2020
            }
        }
    )

BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book!', 5, 2030),
    Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book!', 5, 2030),
    Book(3, 'Master Endpoints', 'codingwithroby', 'A awesome book!', 5, 2029),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2, 2028),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3, 2027),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1, 2026)
]

@app.get("/books", status_code = status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

@app.get("/books/{book_id}", status_code = status.HTTP_200_OK)
async def read_books(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code = 404, detail = f'Book_id {book_id} is Not Found')

@app.get("/books/", status_code = status.HTTP_200_OK)
async def read_books_by_rating(book_rating: int = Query(gt=0, lt=6)):
    books_rating = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_rating.append(book)
    return books_rating

@app.get("/books/publish/", status_code=status.HTTP_200_OK)
async def read_books_by_publish_date(published_date:int = Query(gt=2004, lt=2030)):
    books_publish_date = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_publish_date.append(book)
    return books_publish_date

@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump()) # previously dict()
    BOOKS.append(set_book_id(new_book))

def set_book_id(book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id+1
    return book

'''
@app.put("/books/update_book/", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book_request: BookRequest, book_id:int = Query(gte=0,lte=len(BOOKS))):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS[i] = book_request
            BOOKS[i].id = book_id
            book_changed = True
            break
    if not book_changed:
        raise HTTPException(status_code=404, detail= f'Book_id {book_id} is Not Found')
    
@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id:int = Path(gt=0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break
    if not book_changed:
        raise HTTPException(status_code=404, detail= f'Book_id {book_id} is Not Found')
'''

def get_book_id(book_id):
    for index, book in enumerate(BOOKS):
        if book.id == book_id:
            return index,book
        return None, None
    
@app.put("/books/update_book/", status_code = status.HTTP_204_NO_CONTENT )
async def update_book(book_request: BookRequest, book_id:int = Query(gt=0)):
    index, book = get_book_id(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail= f'Book_id {book_id} is Not Found')
    updated_book = Book(**book_request.model_dump())
    updated_book.id = book_id
    BOOKS[index] = updated_book


@app.delete("/books/{book_id}", status_code = status.HTTP_204_NO_CONTENT )
async def delete_book(book_id:int = Query(gt=0)):
    index, book = get_book_id(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail= f'Book_id {book_id} is Not Found')
    BOOKS.pop(index)
    