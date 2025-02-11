from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, current_user
from datetime import datetime

"""
One-to-Many Relationship
The Book and User Database structures will be modular and connected.
"""

db = SQLAlchemy()

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    genre = db.Column(db.String(255))
    cover_image = db.Column(db.String(255), default="static/uploads/default_book.jpg")
    published_year = db.Column(db.Integer)
    isbn = db.Column(db.String(20), unique=True, nullable=True)
    # db.relationship("ChildModel", backref="parent_model", lazy="select, joined, subquery, or dynamic")
    # lazy = "dynamic": Returns a query object instead of a list, allowing additional filtering.
    # Relationship: One Book -> Many Reviews
    reviews = db.relationship('Review', backref='book', lazy=True)
    # Relationship: One Book -> Many Reading Statuses
    reading_statuses = db.relationship("ReadingStatus", backref="book", lazy="dynamic")
    # Relationship: One Book -> Many Quotes
    quotes = db.relationship("Quote", backref="book", lazy="dynamic")


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())


class ReadingStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), nullable=False) # "Want to Read, Reading, Read"
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.timestamp)

class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.timestamp)