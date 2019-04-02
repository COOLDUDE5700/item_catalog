#!/usr/bin/env python

# importing modules
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


# creating table : user
class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


# creating table : category
class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    User = relationship(User)

# return object data in easily serializable format
    @property
    def serialize(self):
        return{
            'id': self.id,
            'name': self.name,
            'user_id': self.user_id
            }


# create table : item
class Item(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250))
    picture = Column(String(250))
    category_id = Column(Integer, ForeignKey('category.id'))
    Category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    User = relationship(User)


# return object data in easily serializable format
    @property
    def serialize(self):
        return{
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'user_id': self.user_id,
            'category_id': self.category_id
            }

engine = create_engine('sqlite:///item_catalog.db')
Base.metadata.create_all(engine)
