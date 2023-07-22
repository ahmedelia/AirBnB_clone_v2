#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import create_engine, String, Column, Integer, DateTime, Table
from os import getenv


storage_type = getenv("HBNB_TYPE_STORAGE")


class Amenity(BaseModel, Base):
    __tablename__ = "amenities"
    name = Column(String(128), nullable=False)
    if storage_type == "db":
        place_amenities = relationship(
            "Place", back_populates='amenities', viewonly=False, secondary="place_amenity")

    def __init__(self, *args, **kwargs):
        """ Set up an instance with its properties. """
        super().__init__(*args, **kwargs)
