import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas, crud
from .database import engine, Base, get_db



Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bookstore API")


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")


@app.get("/authors/", response_model=List[schemas.Author])
def list_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_authors(db, skip, limit)


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db, author)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def get_author(author_id: int, db: Session = Depends(get_db)):
    db_obj = crud.get_author(db, author_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_obj


@app.put("/authors/{author_id}", response_model=schemas.Author)
def update_author(author_id: int, author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_obj = crud.update_author(db, author_id, author)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_obj


@app.delete("/authors/{author_id}")
def delete_author(author_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_author(db, author_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Author not found")
    return {"ok": True}


@app.get("/categories/", response_model=List[schemas.Category])
def list_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_categories(db, skip, limit)


@app.post("/categories/", response_model=schemas.Category)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    return crud.create_category(db, category)


@app.get("/categories/{category_id}", response_model=schemas.Category)
def get_category(category_id: int, db: Session = Depends(get_db)):
    db_obj = crud.get_category(db, category_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_obj


@app.put("/categories/{category_id}", response_model=schemas.Category)
def update_category(category_id: int, category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    db_obj = crud.update_category(db, category_id, category)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_obj


@app.delete("/categories/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_category(db, category_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"ok": True}


@app.get("/books/", response_model=List[schemas.Book])
def list_books(
    skip: int = 0,
    limit: int = 100,
    author_id: int | None = None,
    category_id: int | None = None,
    title: str | None = None,
    year: int | None = None,
    min_price: int | None = None,
    max_price: int | None = None,
    db: Session = Depends(get_db),
):
    books = crud.find_books(
        db,
        skip=skip,
        limit=limit,
        author_id=author_id,
        category_id=category_id,
        title=title,
        year=year,
        min_price=min_price,
        max_price=max_price,
    )
    return books


@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db, book)


@app.get("/books/{book_id}", response_model=schemas.Book)
def get_book(book_id: int, db: Session = Depends(get_db)):
    db_obj = crud.get_book(db, book_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_obj


@app.get("/books/{book_id}/image")
def serve_book_image(book_id: int, db: Session = Depends(get_db)):
    raise HTTPException(status_code=404, detail="Image endpoint removed; images are stored as strings/URLs")


@app.put("/books/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_obj = crud.update_book(db, book_id, book)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_obj


@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_book(db, book_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"ok": True}


 


@app.get("/customers/", response_model=List[schemas.Customer])
def list_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_customers(db, skip, limit)


@app.post("/customers/", response_model=schemas.Customer)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    return crud.create_customer(db, customer)


@app.get("/customers/{customer_id}", response_model=schemas.Customer)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    db_obj = crud.get_customer(db, customer_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_obj


@app.put("/customers/{customer_id}", response_model=schemas.Customer)
def update_customer(customer_id: int, customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    db_obj = crud.update_customer(db, customer_id, customer)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_obj


@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_customer(db, customer_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"ok": True}


@app.get("/orders/", response_model=List[schemas.BookOrder])
def list_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_orders(db, skip, limit)


@app.post("/orders/", response_model=schemas.BookOrder)
def create_order(order: schemas.BookOrderCreate, db: Session = Depends(get_db)):
    return crud.create_order(db, order)


@app.get("/orders/{order_id}", response_model=schemas.BookOrder)
def get_order(order_id: int, db: Session = Depends(get_db)):
    db_obj = crud.get_order(db, order_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_obj


@app.put("/orders/{order_id}", response_model=schemas.BookOrder)
def update_order(order_id: int, order: schemas.BookOrderCreate, db: Session = Depends(get_db)):
    db_obj = crud.update_order(db, order_id, order)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_obj


@app.delete("/orders/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_order(db, order_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"ok": True}


@app.get("/orderings/", response_model=List[schemas.Ordering])
def list_orderings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_orderings(db, skip, limit)


@app.post("/orderings/", response_model=schemas.Ordering)
def create_ordering(ordering: schemas.OrderingCreate, db: Session = Depends(get_db)):
    return crud.create_ordering(db, ordering)


@app.delete("/orderings/{book_id}/{order_id}/{customer_id}")
def delete_ordering(book_id: int, order_id: int, customer_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_ordering(db, book_id, order_id, customer_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Ordering not found")
    return {"ok": True}


# Login endpoint
@app.post("/login", response_model=schemas.CustomerOut)
def login(payload: schemas.LoginRequest, db: Session = Depends(get_db)):
    cust = crud.authenticate_customer(db, payload.user, payload.password)
    if not cust:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return cust


# Return orders for a given customer with book title and price
@app.get("/customers/{customer_id}/orders_info", response_model=List[schemas.CustomerOrder])
def customer_orders(customer_id: int, db: Session = Depends(get_db)):
    # verify customer exists
    cust = crud.get_customer(db, customer_id)
    if not cust:
        raise HTTPException(status_code=404, detail="Customer not found")
    return crud.get_customer_orders(db, customer_id)
