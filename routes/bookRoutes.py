from pydantic import BaseModel, Field
from typing import Optional
from fastapi import APIRouter, Depends, Query, Path
from config.database import Session as Session
from models.book import Book as BookModel
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from auth.jwtBearer import JWTBearer




class Book(BaseModel):
    title: str = Field(max_length=100, min_length=1, default="Título del libro")
    author: str = Field(max_length=100, min_length=3, default="Autor del libro")
    year: int = Field(ge=1400, le=2100, default=2000)
    category: str = Field(max_length=50, min_length=3, default="Categoría del libro")
    numOfPages: int = Field(ge=1, default=100)

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
def get_book(id: int = Path(ge=1, le=2100)):
    db = Session()
    result = db.query(BookModel).filter(BookModel.code == id).first()
    db.close()
    if not result:
        return JSONResponse(status_code=404, content={"message": "No encontrado"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@router.get("/book/", tags=["Books"])
def get_book_category(category: str = Query(min_length=3, max_length=20)):
    db = Session()
    result = db.query(BookModel).filter(BookModel.category == category).all()
    db.close()
    if not result:
        return JSONResponse(status_code=404, content={"message": "No encontrado"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@router.post("/books", tags=["Books"])
def create_book(book: Book):
    db = Session()
    newBook = BookModel(**book.model_dump())
    db.add(newBook)
    db.commit()
    return JSONResponse(status_code=201,content=jsonable_encoder(newBook))


@router.patch("/books/{id}",tags=["Books"])
def update_book(id: int, book: Book):
    db= Session()
    result = db.query(BookModel).filter(BookModel.code == id).first()
    if not result: 
        JSONResponse(status_code=404,content={"message":"no encontrado"})
    result.title =  book.title
    result.author = book.author
    result.year = book.year
    result.category = book.category
    result.numOfPages = book.numOfPages
    db.commit()

    return JSONResponse(status_code=200,content=jsonable_encoder(result))

@router.delete("/books/{id}",tags=["Books"])
def delete_computer(id:int):
    db = Session()
    result = db.query(BookModel).filter(BookModel.code == id).first()
    if not result: 
        JSONResponse(status_code=404,content={"message":"no encontrado"})
    db.delete(result)
    db.commit()

    return JSONResponse(content = {"message":"Libro eliminado correctamente"}, status_code=200)

