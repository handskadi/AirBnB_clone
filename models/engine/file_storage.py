#!/usr/bin/python3
""" File Storage Class Module """
import datetime
import json
import os

class FileStorage:

    """ Storage class to get data """
    __file_path = "file.json"
    __objects = {}


    def all(self):
        """ This returns _objects dictionary """
        return FileStorage.__objects

    def new(self, obj):
        key = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        with open(FileStorage.__file_path, "w", encoding="utf-8") as f:
            mydic = {key: value.to_dict() for key, value in FileStorage.__objects.items()}
            json.dump(mydic, f)

    def classes(self):
        from models.base_model import BaseModel
        classes = {"BaseModel": BaseModel}
        return classes

    def reload(self):
        if not os.path.isfile(FileStorage.__file_path):
            return
        with open(FileStorage.__file_path, "r", encoding="utf-8") as f:
            obj_d = json.load(f)
            obj_d = {key: self.classes()[value["__class__"]](**value)
                        for key, value in obj_d.items()}
            FileStorage.__objects = obj_d

