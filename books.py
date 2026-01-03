from fastapi import FastAPI, Body

app = FastAPI()

BOOKS = [
    {'title':'Title One', 'author':'Author One', 'category':'science'},
    {'title':'Title Two', 'author':'Author Six', 'category':'science'},
    {'title':'Title Three', 'author':'Author Three', 'category':'history'},
    {'title':'Title Four', 'author':'Author Four', 'category':'math'},
    {'title':'Title Five', 'author':'Author Five', 'category':'math'},
    {'title':'Title Six', 'author':'Author Six', 'category':'math'},
]

@app.get("/")
async def welcome():
    return "Welcome to the book store!!!"

# Even if we dont specify also it is by default async only
@app.get("/books") # returns all the books
async def read_all_books():
    return BOOKS

@app.get("/books/{book_title}") #return the book object if the title is found (path parameters)
async def read_book_by_title(book_title:str): # type validation
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book
    else:
        return f"The book with the title '{book_title}' is not found!!!"
    
@app.get("/books/") # accept the query parameters dynamically (?key=value)
async def read_book_by_category(category: str):
    books_category = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_category.append(book)
    return books_category

# using query params
@app.get("/books/byauthor/")
async def read_books_by_author(author:str):
    books_author = []
    for book in BOOKS:
        if book.get('author').casefold() == author.casefold():
            books_author.append(book)
    return books_author

# filter by author_name and category
@app.get("/books/{book_author}/")
async def read_books_by_author_category(book_author:str, category:str):
    books_author_category = []
    for book in BOOKS:
        if book.get('author').casefold() == book_author.casefold() and \
                book.get('category').casefold() == category.casefold():
            books_author_category.append(book)
    return books_author_category

@app.post("/books/create_book")
async def create_book(new_book = Body()):
    BOOKS.append(new_book)
    return "Successfully Added"

@app.put("/books/update_book/{book_title}")
async def update_book(book_title,updated_book = Body()):
    flag = False
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            flag = True
            BOOKS[i] = updated_book
    if not flag:
        return f"The book with the title {book_title} is not found"
    return "Book Updated"

@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title:str):
    flag = False
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            flag = True
            BOOKS.pop(i)
            break
    if not flag:
        return f"The book with the title {book_title} is not found"
    return "Book Deleted!!!"