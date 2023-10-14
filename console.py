#!/usr/bin/python3

import cmd
from models.base_model import BaseModel
from models import storage
import json

class HBNBCommand(cmd.Cmd):
    prompt = "(mkbnb) "

    def do_quit(self, line):
        """ type (quit) to exis the program """
        return True

    def do_EOF(self, line):
        """ Deals with EOF char """
        print() # to handle newline 
        return True


if __name__ == '__main__':
        HBNBCommand().cmdloop()
