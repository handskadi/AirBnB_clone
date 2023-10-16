#!/usr/bin/python3
"""File Storage Class Module."""
import datetime
import json
import os
import models


class FileStorage:
    """Storage class to get data."""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """All func  returns _objects dictionary."""
        return FileStorage.__objects

    def new(self, obj):
        """Obj with key <objclassname> id."""
        key = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """From obj to Json."""
        with open(FileStorage.__file_path, "w", encoding="utf-8") as f:
            mydic = {key: value.to_dict()
                     for key, value in FileStorage.__objects.items()}
            json.dump(mydic, f)

    def classes(self):
        """Dic of classes & thier refs."""
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review
        classes = {
                "BaseModel": BaseModel,
                "User": User,
                "State": State,
                "City": City,
                "Amenity": Amenity,
                "Place": Place,
                "Review": Review
                }
        return classes

    def attributes(self):
        """Return Valid attributes and their types for classname."""
        attributes = {
                "BaseModel": {
                    "id": str,
                    "created_at": datetime.datetime,
                    "updated_at": datetime.datetime
                },
                "User": {
                    "email": str,
                    "password": str,
                    "first_name": str,
                    "last_name": str
                },
                "State": {
                    "name": str
                },
                "City": {
                    "state_id": str,
                    "name": str
                },
                "Amenity": {
                    "name": str
                },
                "Place":
                {
                    "city_id": str,
                    "user_id": str,
                    "name": str,
                    "description": str,
                    "number_rooms": int,
                    "number_bathrooms": int,
                    "max_guest": int,
                    "price_by_night": int,
                    "latitude": float,
                    "longitude": float,
                    "amenity_ids": list
                },
                "Review":
                {
                    "place_id": str,
                    "user_id": str,
                    "text": str
                }
        }
        return attributes

    def reload(self):
        """Reload the object from Json."""
        if not os.path.isfile(FileStorage.__file_path):
            return
        with open(FileStorage.__file_path, "r", encoding="utf-8") as f:
            obj_d = json.load(f)
            obj_d = {key: self.classes()[value["__class__"]](**value)
                     for key, value in obj_d.items()}
            FileStorage.__objects = obj_d
