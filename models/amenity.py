#!/usr/bin/python
""" Module: amenity - holds class Amenity """

import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """
    Representation of the Amenity class.
    """

    if models.selected_storage == 'db':
        __tablename__ = 'amenities'
        name = Column(String(128), nullable=False)
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """
        Initializes an instance of the Amenity class.
        """
        super().__init__(*args, **kwargs)
