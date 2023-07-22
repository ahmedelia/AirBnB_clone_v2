#!/usr/bin/python3
"""This module defines a class to manage db storage for hbnb clone"""
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from models.base_model import Base, BaseModel
from os import getenv
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User
from models.amenity import Amenity


class DBStorage:
    """This class manages storage of hbnb models"""
    __engine = None
    __session = None
    classes = ["State", "User", "City", "Place", "Review", "Amenity"]

    def __init__(self):

        HBNB_MYSQL_USER = getenv("HBNB_MYSQL_USER")
        HBNB_MYSQL_PWD = getenv("HBNB_MYSQL_PWD")
        HBNB_MYSQL_HOST = getenv("HBNB_MYSQL_HOST")
        HBNB_MYSQL_DB = getenv("HBNB_MYSQL_DB")
        HBNB_ENV = getenv("HBNB_ENV")
        db_url = 'mysql+mysqldb://{}:{}@{}/{}'.format(
            HBNB_MYSQL_USER, HBNB_MYSQL_PWD, HBNB_MYSQL_HOST, HBNB_MYSQL_DB)
        self.__engine = create_engine(db_url, pool_pre_ping=True)
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def delete(self, obj=None):
        """Delete a Obj from __Objects"""
        if obj != None:
            self.__session.delete(obj)

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        dictionary = {}
        if cls != None:
            query = self.__session.query(cls).all()
            for obj in query:
                dictionary[obj.id + '.' + cls.__name__] = obj
        else:
            query = []
            for tbl in self.classes:
                query += self.__session.query(eval(tbl)).all()
                for obj in query:
                    dictionary[obj.id + '.' + tbl] = obj
        return dictionary

    def new(self, obj):
        """Adds new object to session"""
        self.__session.add(obj)

    def save(self):
        """commit changes to db"""
        self.__session.commit()

    def reload(self):
        """create session scoped to perform crud"""
        Base.metadata.create_all(self.__engine)
        self.__session = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(self.__session)()

    def close(self):
        """Close"""
        self.__session.close()
