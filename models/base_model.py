#!/usr/bin/python3
"""
Module: base_model - contains the BaseModel class
"""

from datetime import datetime
import models
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import uuid

time = "%Y-%m-%dT%H:%M:%S.%f"

if models.selected_storage == "db":
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """
    The BaseModel class serves as the foundation for future classes.
    """

    if models.selected_storage == "db":
        id = Column(String(60), primary_key=True)
        created_at = Column(DateTime, default=datetime.utcnow)
        updated_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """
        Initializes an instance of the BaseModel class.
        """
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if kwargs.get("created_at", None) and type(self.created_at) is str:
                self.created_at = datetime.strptime(kwargs["created_at"], time)
            else:
                self.created_at = datetime.utcnow()
            if kwargs.get("updated_at", None) and type(self.updated_at) is str:
                self.updated_at = datetime.strptime(kwargs["updated_at"], time)
            else:
                self.updated_at = datetime.utcnow()
            if kwargs.get("id", None) is None:
                self.id = str(uuid.uuid4())
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at

    def __str__(self):
        """
        Returns a string representation of the BaseModel class.
        """
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)

    def save(self):
        """
        Updates the 'updated_at' attribute with the current datetime and
        saves the instance.
        """
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self, save_check=False):
        """
        Returns a dictionary containing all keys/values of the instance,
        formatted for serialization.
        """
        parsed_dict = self.__dict__.copy()
        if "created_at" in parsed_dict:
            parsed_dict["created_at"] = (
                parsed_dict["created_at"].strftime(time)
            )
        if "updated_at" in parsed_dict:
            parsed_dict["updated_at"] = (
                parsed_dict["updated_at"].strftime(time)
            )
        parsed_dict["__class__"] = self.__class__.__name__
        if "_sa_instance_state" in parsed_dict:
            del parsed_dict["_sa_instance_state"]
        if "password" in parsed_dict and save_check is False:
            del parsed_dict["password"]
        return parsed_dict

    def delete(self):
        """
        Deletes the current instance from storage.
        """
        models.storage.delete(self)
