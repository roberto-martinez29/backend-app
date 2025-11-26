from typing import List, Optional
from datetime import date
from pydantic import BaseModel


# Author
class AuthorBase(BaseModel):
    authorName: str


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    authorID: int

    class Config:
        orm_mode = True


# Category
class CategoryBase(BaseModel):
    categoryDescription: str


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    categoryID: int

    class Config:
        orm_mode = True


# Book
class BookBase(BaseModel):
    categoryID: int
    title: str
    isbn: Optional[str] = None
    year: Optional[int] = None
    price: int
    noPages: Optional[int] = None
    bookDescription: Optional[str] = None


class BookCreate(BookBase):
    authorIDs: Optional[List[int]] = []


class Book(BookBase):
    bookID: int
    # single author name (string). If a book has multiple authors, names are joined by ", "
    author: Optional[str] = None
    # category name/description
    category: Optional[str] = None
    # image URL for retrieving the image (empty string when absent)
    image_url: str = ""

    class Config:
        orm_mode = True


# Customer
class CustomerBase(BaseModel):
    firstName: str
    lastName: str
    zipCode: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    address: Optional[str] = None
    user: Optional[str] = None
    password: Optional[str] = None


class CustomerCreate(CustomerBase):
    pass


class Customer(CustomerBase):
    customerID: int

    class Config:
        orm_mode = True


# BookOrder
class BookOrderBase(BaseModel):
    customerID: int
    orderDate: Optional[date] = None


class BookOrderCreate(BookOrderBase):
    bookIDs: Optional[List[int]] = []


class BookOrder(BookOrderBase):
    orderID: int

    class Config:
        orm_mode = True


# Ordering (association) - simple representation
class OrderingBase(BaseModel):
    bookID: int
    orderID: int
    customer_id: int


class OrderingCreate(OrderingBase):
    pass


class Ordering(OrderingBase):
    class Config:
        orm_mode = True
