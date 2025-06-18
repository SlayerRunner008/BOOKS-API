from pydantic import BaseModel, Field
from fastapi import APIRouter, Query, Path
from config.database import Session
from models.book import Book as BookModel
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

class Book(BaseModel):
    title: str = Field(max_length=100, min_length=1)
    author: str = Field(max_length=100, min_length=3)
    year: int = Field(ge=1400, le=2100)
    category: str = Field(max_length=50, min_length=3)
    numOfPages: int = Field(ge=1)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Clean Code",
                "author": "Robert C. Martin",
                "year": 2008,
                "category": "Software Development",
                "numOfPages": 464
            }
        }

router = APIRouter()

@router.get("/books", tags=["Books"])
def get_books():
    db = Session()
    result = db.query(BookModel).all()
    db.close()
    return JSONResponse(content=jsonable_encoder(result), status_code=200)

@router.get("/books/{id}", tags=["Books"])
def get_book(id: int = Path(ge=1)):
    db = Session()
    result = db.query(BookModel).filter(BookModel.code == id).first()
    db.close()
    if not result:
        return JSONResponse(status_code=404, content={"message": "No encontrado"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@router.get("/book/", tags=["Books"])
def get_book_category(category: str = Query(min_length=3, max_length=50)):
    db = Session()
    result = db.query(BookModel).filter(BookModel.category == category).all()
    db.close()
    if not result:
        return JSONResponse(status_code=404, content={"message": "No encontrado"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@router.post("/books", tags=["Books"])
def create_book(book: Book):
    db = Session()
    new_book = BookModel(**book.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    db.close()
    return JSONResponse(status_code=201, content=jsonable_encoder(new_book))

@router.patch("/books/{id}", tags=["Books"])
def update_book(id: int, book: Book):
    db = Session()
    result = db.query(BookModel).filter(BookModel.code == id).first()
    if not result:
        db.close()
        return JSONResponse(status_code=404, content={"message": "No encontrado"})
    
    result.title = book.title
    result.author = book.author
    result.year = book.year
    result.category = book.category
    result.numOfPages = book.numOfPages

    db.commit()
    db.refresh(result)
    db.close()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@router.delete("/books/{id}", tags=["Books"])
def delete_book(id: int):
    db = Session()
    result = db.query(BookModel).filter(BookModel.code == id).first()
    if not result:
        db.close()
        return JSONResponse(status_code=404, content={"message": "No encontrado"})
    
    db.delete(result)
    db.commit()
    db.close()
    return JSONResponse(content={"message": "Libro eliminado correctamente"}, status_code=200)
