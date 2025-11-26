from sqlalchemy import Column, Integer, String, ForeignKey, LargeBinary, Date
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Table
from .database import Base


class Author(Base):
    __tablename__ = "author"
    authorID = Column(Integer, primary_key=True, index=True)
    authorName = Column(String(45), nullable=False)
    books = relationship("Book", secondary="author_book", back_populates="authors")


author_book = Table(
    "author_book",
    Base.metadata,
    Column("authorID", Integer, ForeignKey("author.authorID"), primary_key=True),
    Column("bookID", Integer, ForeignKey("book.bookID"), primary_key=True),
)


class Category(Base):
    __tablename__ = "category"
    categoryID = Column(Integer, primary_key=True, index=True)
    categoryDescription = Column(String(45), nullable=False)
    books = relationship("Book", back_populates="category")


class Book(Base):
    __tablename__ = "book"
    bookID = Column(Integer, primary_key=True, index=True)
    categoryID = Column(Integer, ForeignKey("category.categoryID"), nullable=False)
    title = Column(String(45), nullable=False)
    isbn = Column(String(45))
    year = Column(Integer)
    price = Column(Integer, nullable=False)
    noPages = Column(Integer)
    bookDescription = Column(String(500))
    image = Column(LargeBinary)

    category = relationship("Category", back_populates="books")
    authors = relationship("Author", secondary="author_book", back_populates="books")
    orderings = relationship("Ordering", back_populates="book")


class Customer(Base):
    __tablename__ = "customer"
    customerID = Column(Integer, primary_key=True, index=True)
    firstName = Column(String(45), nullable=False)
    lastName = Column(String(45), nullable=False)
    zipCode = Column(String(45))
    city = Column(String(45))
    state = Column(String(45))
    address = Column(String(100))
    user = Column(String(45))
    password = Column(String(45))
    orders = relationship("BookOrder", back_populates="customer")


class BookOrder(Base):
    __tablename__ = "book_order"
    orderID = Column(Integer, primary_key=True, index=True)
    customerID = Column(Integer, ForeignKey("customer.customerID"), nullable=False)
    orderDate = Column(Date)

    customer = relationship("Customer", back_populates="orders")
    order_items = relationship("Ordering", back_populates="order")


class Ordering(Base):
    __tablename__ = "ordering"
    bookID = Column(Integer, ForeignKey("book.bookID"), primary_key=True)
    orderID = Column(Integer, ForeignKey("book_order.orderID"), primary_key=True)
    customer_id = Column(Integer, primary_key=True)

    book = relationship("Book", back_populates="orderings")
    order = relationship("BookOrder", back_populates="order_items")
