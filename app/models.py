from sqlalchemy import Column, Integer, String, ForeignKey, LargeBinary, Date
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Table
from .database import Base


class Author(Base):
    __tablename__ = "author"
    authorID = Column("authorid", Integer, primary_key=True, index=True)
    authorName = Column("authorname", String(45), nullable=False)
    books = relationship("Book", secondary="author_book", back_populates="authors")


author_book = Table(
    "author_book",
    Base.metadata,
    Column("authorid", Integer, ForeignKey("author.authorid"), primary_key=True),
    Column("bookid", Integer, ForeignKey("book.bookid"), primary_key=True),
)


class Category(Base):
    __tablename__ = "category"
    categoryID = Column("categoryid", Integer, primary_key=True, index=True)
    categoryDescription = Column("categorydescription", String(45), nullable=False)
    books = relationship("Book", back_populates="category")


class Book(Base):
    __tablename__ = "book"
    bookID = Column("bookid", Integer, primary_key=True, index=True)
    categoryID = Column("categoryid", Integer, ForeignKey("category.categoryid"), nullable=False)
    title = Column(String(45), nullable=False)
    isbn = Column(String(45))
    year = Column(Integer)
    price = Column(Integer, nullable=False)
    noPages = Column("nopages", Integer)
    bookDescription = Column("bookdescription", String(500))
    image = Column("image", LargeBinary)

    category = relationship("Category", back_populates="books")
    authors = relationship("Author", secondary="author_book", back_populates="books")
    orderings = relationship("Ordering", back_populates="book")


class Customer(Base):
    __tablename__ = "customer"
    customerID = Column("customerid", Integer, primary_key=True, index=True)
    firstName = Column("firstname", String(45), nullable=False)
    lastName = Column("lastname", String(45), nullable=False)
    zipCode = Column("zipcode", String(45))
    city = Column("city", String(45))
    state = Column("state", String(45))
    address = Column("address", String(100))
    user = Column("user", String(45))
    password = Column("password", String(45))
    orders = relationship("BookOrder", back_populates="customer")


class BookOrder(Base):
    __tablename__ = "book_order"
    orderID = Column("orderid", Integer, primary_key=True, index=True)
    customerID = Column("customerid", Integer, ForeignKey("customer.customerid"), nullable=False)
    orderDate = Column("orderdate", Date)

    customer = relationship("Customer", back_populates="orders")
    order_items = relationship("Ordering", back_populates="order")


class Ordering(Base):
    __tablename__ = "ordering"
    bookID = Column("bookid", Integer, ForeignKey("book.bookid"), primary_key=True)
    orderID = Column("orderid", Integer, ForeignKey("book_order.orderid"), primary_key=True)
    customer_id = Column("customerid", Integer, primary_key=True)

    book = relationship("Book", back_populates="orderings")
    order = relationship("BookOrder", back_populates="order_items")
