#!/usr/bin/python3
"""File Storage Class Module."""
import datetime
import json
import os


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
        classes = {"BaseModel": BaseModel}
        return classes

    def attributes(self):
        """Return Valid attributes and their types for classname."""
        attributes = {
                "BaseModel": {
                    "id": str,
                    "created_at": datetime.datetime,
                    "updated_at": datetime.datetime
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
