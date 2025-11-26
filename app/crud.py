from sqlalchemy.orm import Session
from typing import List
from . import models, schemas


# Authors
def get_authors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Author).offset(skip).limit(limit).all()


def get_author(db: Session, author_id: int):
    return db.query(models.Author).filter(models.Author.authorID == author_id).first()


def create_author(db: Session, author: schemas.AuthorCreate):
    db_obj = models.Author(authorName=author.authorName)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_author(db: Session, author_id: int, author: schemas.AuthorCreate):
    db_obj = get_author(db, author_id)
    if not db_obj:
        return None
    db_obj.authorName = author.authorName
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_author(db: Session, author_id: int):
    db_obj = get_author(db, author_id)
    if not db_obj:
        return False
    db.delete(db_obj)
    db.commit()
    return True


# Category
def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Category).offset(skip).limit(limit).all()


def get_category(db: Session, category_id: int):
    return db.query(models.Category).filter(models.Category.categoryID == category_id).first()


def create_category(db: Session, category: schemas.CategoryCreate):
    db_obj = models.Category(categoryDescription=category.categoryDescription)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_category(db: Session, category_id: int, category: schemas.CategoryCreate):
    db_obj = get_category(db, category_id)
    if not db_obj:
        return None
    db_obj.categoryDescription = category.categoryDescription
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_category(db: Session, category_id: int):
    db_obj = get_category(db, category_id)
    if not db_obj:
        return False
    db.delete(db_obj)
    db.commit()
    return True


# Books
def get_books(db: Session, skip: int = 0, limit: int = 100):
    books = db.query(models.Book).offset(skip).limit(limit).all()
    return [_book_to_dict(b) for b in books]


def find_books(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    author_id: int | None = None,
    category_id: int | None = None,
    title: str | None = None,
    year: int | None = None,
    min_price: int | None = None,
    max_price: int | None = None,
):
    q = db.query(models.Book)
    if author_id is not None:
        q = q.join(models.Book.authors).filter(models.Author.authorID == author_id)
    if category_id is not None:
        q = q.filter(models.Book.categoryID == category_id)
    if title:
        q = q.filter(models.Book.title.ilike(f"%{title}%"))
    if year is not None:
        q = q.filter(models.Book.year == year)
    if min_price is not None:
        q = q.filter(models.Book.price >= min_price)
    if max_price is not None:
        q = q.filter(models.Book.price <= max_price)
    books = q.offset(skip).limit(limit).all()
    return [_book_to_dict(b) for b in books]


def get_book(db: Session, book_id: int):
    b = db.query(models.Book).filter(models.Book.bookID == book_id).first()
    if not b:
        return None
    return _book_to_dict(b)


def create_book(db: Session, book: schemas.BookCreate):
    db_obj = models.Book(
        categoryID=book.categoryID,
        title=book.title,
        isbn=book.isbn,
        year=book.year,
        price=book.price,
        noPages=book.noPages,
        bookDescription=book.bookDescription,
    )
    if book.authorIDs:
        authors = db.query(models.Author).filter(models.Author.authorID.in_(book.authorIDs)).all()
        db_obj.authors = authors
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return _book_to_dict(db_obj)


def update_book(db: Session, book_id: int, book: schemas.BookCreate):
    # fetch real model (get_book returns transformed dict)
    real = db.query(models.Book).filter(models.Book.bookID == book_id).first()
    if not real:
        return None
    real.categoryID = book.categoryID
    real.title = book.title
    real.isbn = book.isbn
    real.year = book.year
    real.price = book.price
    real.noPages = book.noPages
    real.bookDescription = book.bookDescription
    if book.authorIDs is not None:
        authors = db.query(models.Author).filter(models.Author.authorID.in_(book.authorIDs)).all()
        real.authors = authors
    db.commit()
    db.refresh(real)
    return _book_to_dict(real)


def delete_book(db: Session, book_id: int):
    real = db.query(models.Book).filter(models.Book.bookID == book_id).first()
    if not real:
        return False
    db.delete(real)
    db.commit()
    return True


# Image retrieval helper (returns raw bytes or None)
def get_book_image(db: Session, book_id: int):
    real = db.query(models.Book).filter(models.Book.bookID == book_id).first()
    if not real:
        return None
    return real.image


def _book_to_dict(b: models.Book) -> dict:
    # Convert Book model into dict with single author string, category name and base64 image
    # author names joined by ', '
    author_names = [a.authorName for a in (b.authors or [])]
    author_str = None
    if author_names:
        author_str = ", ".join(author_names)

    category_desc = None
    if getattr(b, "category", None):
        try:
            category_desc = b.category.categoryDescription
        except Exception:
            category_desc = None

    # image_url points to the existing image endpoint for this book
    image_url = f"/books/{b.bookID}/image"

    return {
        "bookID": b.bookID,
        "categoryID": b.categoryID,
        "title": b.title,
        "isbn": b.isbn,
        "year": b.year,
        "price": b.price,
        "noPages": b.noPages,
        "bookDescription": b.bookDescription,
        "author": author_str,
        "category": category_desc,
        "image_url": image_url,
    }



# Customer
def get_customers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Customer).offset(skip).limit(limit).all()


def get_customer(db: Session, customer_id: int):
    return db.query(models.Customer).filter(models.Customer.customerID == customer_id).first()


def create_customer(db: Session, customer: schemas.CustomerCreate):
    db_obj = models.Customer(**customer.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_customer(db: Session, customer_id: int, customer: schemas.CustomerCreate):
    db_obj = get_customer(db, customer_id)
    if not db_obj:
        return None
    for k, v in customer.dict().items():
        setattr(db_obj, k, v)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_customer(db: Session, customer_id: int):
    db_obj = get_customer(db, customer_id)
    if not db_obj:
        return False
    db.delete(db_obj)
    db.commit()
    return True


# Orders (book_order)
def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.BookOrder).offset(skip).limit(limit).all()


def get_order(db: Session, order_id: int):
    return db.query(models.BookOrder).filter(models.BookOrder.orderID == order_id).first()


def create_order(db: Session, order: schemas.BookOrderCreate):
    db_obj = models.BookOrder(customerID=order.customerID, orderDate=order.orderDate)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    # if bookIDs provided, create ordering rows
    if order.bookIDs:
        for b in order.bookIDs:
            ord_row = models.Ordering(bookID=b, orderID=db_obj.orderID, customer_id=order.customerID)
            db.add(ord_row)
        db.commit()
    return db_obj


def update_order(db: Session, order_id: int, order: schemas.BookOrderCreate):
    db_obj = get_order(db, order_id)
    if not db_obj:
        return None
    db_obj.customerID = order.customerID
    db_obj.orderDate = order.orderDate
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_order(db: Session, order_id: int):
    db_obj = get_order(db, order_id)
    if not db_obj:
        return False
    # delete ordering rows referencing this order
    db.query(models.Ordering).filter(models.Ordering.orderID == order_id).delete()
    db.delete(db_obj)
    db.commit()
    return True


# Ordering (association)
def get_orderings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Ordering).offset(skip).limit(limit).all()


def create_ordering(db: Session, ordering: schemas.OrderingCreate):
    db_obj = models.Ordering(bookID=ordering.bookID, orderID=ordering.orderID, customer_id=ordering.customer_id)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_ordering(db: Session, book_id: int, order_id: int, customer_id: int):
    db_obj = db.query(models.Ordering).filter(
        models.Ordering.bookID == book_id,
        models.Ordering.orderID == order_id,
        models.Ordering.customer_id == customer_id,
    ).first()
    if not db_obj:
        return False
    db.delete(db_obj)
    db.commit()
    return True
