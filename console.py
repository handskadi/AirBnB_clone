#!/usr/bin/python3

import cmd
from models.base_model import BaseModel
from models import storage
import json
import os
import re

class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb) "

    def emptyline(self):
        """ Nothing will happen in an Emptyline by hitting Enter """
        pass

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

    def do_show(self, cln): 
        """
        Show details of an instance in JSON File
        
        Usage:
            To show an instance, use the following format:
            show <class name> <instance ID>
        """
        if cln == "" or cln is None:
            print("** class name missing **")
        else:
            command = cln.split(' ')
            if command[0] not in storage.classes():
                print("** class doesn't exist **")
            elif len(command) < 2:
                print("** instance id missing **")
            else:
                inst_id = "{}.{}".format(command[0], command[1])
                if inst_id not in storage.all():
                    print("** no instance found **")
                else:
                    print(storage.all()[inst_id])
    
    def do_destroy(self, cln):
        """ Removes an Inst based on name & id of a class """
        if cln == "" or cln is None:
            print("** class name missing **")
        else:
            command = cln.split(' ')
            if command[0]  not in storage.classes():
                print("** class doesn't exist **")
            elif len(command) < 2:
                print("** instance id missing **")
            else:
                inst_id = "{}.{}".format(command[0], command[1])
                if inst_id not in storage.all():
                    print("** no instance found **")
                else:
                    del storage.all()[inst_id]
                    storage.save()

    def do_all(self, cln):
        """ list all representaions of all instances stored inside our Json file """
        if cln != "" or cln is None:
            # TODO: ( None should be removed after tesing )
            command = cln.split(' ')
            if command[0] not in storage.classes():
                print("** class doesn't exist **")
            else:
                inst_list = [str(obj) for k, obj in storage.all().items()
                        if type(obj).__name__ == command[0]]
                print(inst_list)
        else:
            inst_list = [str(obj) for k, obj in storage.all().items()]
            print(inst_list)
    
    # TODO: do_clear should be removed IT's not part of project 
    def do_clear(self, args):
        """Clear the console screen."""
        if os.name == 'posix': # Unix based sys (linux, macOs
            os.system('clear')
        elif os.name == 'nt': # For Windos
            os.system('cls')
        else:
            print("Clear screen not supported on this operating system")
    
    def do_update(self, cln):
        """Update an instance"""
        if cln == "" or cln is None:
            print("** class name missing **")
            return

        reg_exp = r'^(\S+)(?:\s(\S+)(?:\s(\S+)(?:\s((?:"[^"]*")|(?:(\S)+)))?)?)?'
        match = re.search(reg_exp, cln)
        clname = match.group(1)
        uuid = match.group(2)
        attr = match.group(3)
        val = match.group(4)

        if not match:
            print("** class name missing **")
        elif clname not in storage.classes():
            print("** class doesn't exist **")
        else:
            inst_key = "{}.{}".format(clname, uuid)
            if inst_key not in storage.all():
                print("** no instance found **")
            elif not attr:
                print("** attribute name missing **")
            elif not val:
                print("** value missing **")
            else:
                do_casting = None
                if not re.search('^".*"$', val):
                    if '.' in val:
                        do_casting = float
                    else:
                        do_casting = int
                else:
                    val = val.replace('"', '')
                attrs = storage.attrs()[clname]
                if attr in attrs:
                    val = attrs[attr](val)
                elif do_casting:
                    try:
                        val = cast(val)
                    except ValueError:
                        pass
                setattr(storage.all()[inst_key], attr, val)

if __name__ == '__main__':
        HBNBCommand().cmdloop()
