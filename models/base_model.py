#!/usr/bin/python3
"""
    Base Module that will host commin:
    attributes and methods for other classes
"""

import  uuid
from  datetime import datetime
from models import storage

class BaseModel:
    """
        BaseModel Class to host ID, Created at, Updated at attributes

        Args:
            id (str): object id
            created_at (str): created at this date
            updated_at (str): update all date
        """


    def __init__(self, *args, **kwargs):
        """ Init baseModel Class """
        if kwargs is not None and kwargs != {}:
            for key in kwargs:
                if key  == "created_at":
                    self.__dict__["created_at"] = datetime.strptime(kwargs["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
                elif key == "updated_at":
                    self.__dict__["updated_at"] = datetime.strptime(kwargs["updated_at"], "%Y-%m-%dT%H:%M:%S.%f")
                else:
                    self.__dict__[key] = kwargs[key]
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)

    def __str__(self):
        """ string representation of an instance"""
        return "[{}] ({}) {}".format(type(self).__name__, self.id, self.__dict__)

    def save(self):
        """ updating public instance of updated at """
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """ prepares a dic represenation of the instance """
        dic = self.__dict__.copy()
        dic["__class__"] = type(self).__name__
        dic["created_at"] = dic["created_at"].isoformat()
        dic["updated_at"] = dic["updated_at"].isoformat()

        return dic
