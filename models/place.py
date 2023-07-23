#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from models.review import Review
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import create_engine, String, Column, Integer, Date, ForeignKey, Float, Table
from os import getenv


storage_type = getenv("HBNB_TYPE_STORAGE")


place_amenity = Table('place_amenity',
                      Base.metadata,
                      Column('place_id', String(60), ForeignKey(
                          'places.id'), nullable=False, primary_key=True),
                      Column('amenity_id', String(60), ForeignKey(
                          'amenities.id'), nullable=False, primary_key=True),
                      )


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    amenity_ids = []
    @property
    def owner(self):
        from models import storage
        from models.user import User
        users = storage.all(User).values()
        for user in users:
            if self.user_id == user.id:
                return user.first_name + " " + user.last_name
        return "not found"

    if storage_type == "db":
        reviews = relationship("Review", backref="place")
    else:
        @property
        def reviews(self):
            """return list of reviews"""
            from models import storage
            reviews = storage.all(Review)
            reviews = [a for a in reviews if a.place_id == self.id]
            return reviews

    if storage_type == "db":
        amenities = relationship("Amenity", secondary="place_amenity",
                                 back_populates='place_amenities', viewonly=False)
    else:
        @property
        def amenities(self):
            """get list of amentities"""
            from models import storage
            from models.amenity import Amenity

            amenities = storage.all(Amenity)
            return [item for item in amenities.values() if item.id in amenity_ids]

        @amenities.setter
        def amenities(self, val):
            """add new amentites to the list"""
            if type(val) != eval("Amenity"):
                return
            amenity_ids.append(val.id)

    def __init__(self, *args, **kwargs):
        """ Set up an instance with its properties. """
        super().__init__(*args, **kwargs)
