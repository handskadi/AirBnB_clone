#!/usr/bin/python3
"""Module creates User class"""
from models.base_model import BaseModel


class User(BaseModel):
    """Class for managing users objects"""

    email = ""
    password = ""
    first_name = ""
    last_name = ""
