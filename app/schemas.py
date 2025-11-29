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


# Customer output (excludes password)
class CustomerOut(BaseModel):
    customerID: int
    firstName: str
    lastName: str
    zipCode: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    address: Optional[str] = None
    user: Optional[str] = None

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


# Items inside an order returned to client
class OrderItem(BaseModel):
    title: str
    price: int


class CustomerOrder(BaseModel):
    orderID: int
    items: List[OrderItem]

    class Config:
        orm_mode = True


# Login
class LoginRequest(BaseModel):
    user: str
    password: str


# Ordering (association) - simple representation
class OrderingBase(BaseModel):
    bookID: int
    orderID: int
    # use `customerid` to match DB/other schemas naming
    customerid: int


class OrderingCreate(OrderingBase):
    pass


class Ordering(OrderingBase):
    class Config:
        orm_mode = True
