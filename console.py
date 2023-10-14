#!/usr/bin/python3

import cmd
from models.base_model import BaseModel
from models import storage
import json

class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb)"

    def do_quit(self, line):
        """ Type (quit) to exit the program """
        return True

    def do_EOF(self, line):
        """ Deals with EOF char """
        print() # to handle newline 
        return True

    def do_create(self, cln):
        """ <create> will create new instance """
        if cln == "" or cln is None:
            print("** class name missing **")
        elif cln not in storage.classes():
            print("** class doesn't exist **")
        else:
            new_instance = storage.classes()[cln]()
            new_instance.save()
            print(new_instance.id)

if __name__ == '__main__':
        HBNBCommand().cmdloop()
