#!/usr/bin/python3
""" Module: state - holds class State """

import models
from models.base_model import BaseModel, Base
from models.city import City
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
import shlex


class State(BaseModel, Base):
    """
    Representation of the State class.
    """

    __tablename__ = 'states'
    name = Column(String(128), nullable=False)

    if models.selected_storage == "db":
        cities = relationship("City", backref="state")
    else:
        @property
        def cities(self):
            """
            Getter for a list of city instances related to the state.
            """
            city_list = []
            all_cities = models.storage.all(City)
            for city in all_cities.values():
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list

    def __init__(self, *args, **kwargs):
        """
        Initializes an instance of the State class.
        """
        super().__init__(*args, **kwargs)
