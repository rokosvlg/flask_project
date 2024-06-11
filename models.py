# -*- coding: UTF-8 -*-
from sqlalchemy import Column,  Integer,Float,Date,  DateTime, Text, Boolean, String, ForeignKey, or_, not_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import relationship, query_expression
from sqlalchemy.sql import func
from database import Base, db_session, engine as db_engine
import datetime
from flask_login import UserMixin
from eng import manager

class Author(Base, UserMixin):
    __tablename__ ='authors'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)

    login = Column(String(32), unique=True)
    password = Column(String(64))

    @manager.user_loader
    def load_author(id):
        return Author.query.get(id)

    def check_password(self, password):
        return password == self.password

class News(Base):
    __tablename__ = 'news'
    id = Column(Integer, primary_key=True)

    title = Column(String(100), default="")
    text = Column(String(1000), default="")
    date = Column(Date, nullable=False)

    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship("Category")

    author_id = Column(Integer, ForeignKey('authors.id'))
    author = relationship("Author")


class Comments(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)

    text = Column(String(100), default="")
    date = Column(Date, nullable=False)

    news_id = Column(Integer, ForeignKey('news.id'))
    news = relationship("News")
    author_id = Column(Integer, ForeignKey('authors.id'))
    author = relationship("Author")

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key = True)
    name = Column(String(20), unique = True)

def init_db():
    from database import engine
    Base.metadata.create_all(bind=engine)
    db_session.commit()

if __name__ == "__main__":
    init_db()