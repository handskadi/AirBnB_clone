#!/usr/bin/python3

import cmd
from models.base_model import BaseModel
from models import storage
import json
import os
import re


class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb) "

    def default(self, cln):
        """Know commad is ntg matches."""
        self._precmd(cln)

    def _precmd(self, cln):
        """Prepare Commands to excute <class>.syn()."""
        alikes = re.search(r"^(\w*)\.(\w+)(?:\(([^)]*)\))$", cln)
        if not alikes:
            return cln
        classname = alikes.group(1)
        method = alikes.group(2)
        args = alikes.group(3)
        valid_uid_and_args = re.search('^"([^"]*)"(?:, (.*))?$', args)
        if valid_uid_and_args:
            uid = valid_uid_and_args.group(1)
            attr_or_dict = valid_uid_and_args.group(2)
        else:
            uid = args
            attr_or_dict = False

        attr_and_value = ""
        if method == "update" and attr_or_dict:
            valid_dict = re.search('^({.*})$', attr_or_dict)
            if valid_dict:
                self.update_dict(classname, uid, valid_dict.group(1))
                return ""
            valid_attr_and_value = re.search(
                    '^(?:"([^"]*)")?(?:, (.*))?$', attr_or_dict)
            if valid_attr_and_value:
                attr_and_value = (valid_attr_and_value.group(
                    1) or "") + " " + (valid_attr_and_value.group(2) or "")
        command = method + " " + classname + " " + uid + " " + attr_and_value
        self.onecmd(command)
        return command

    def update_dict(self, classname, uid, s_dict):
        """Method for Updtae dic."""
        s = s_dict.replace("'", '"')
        d = json.loads(s)
        if not classname:
            print("** class name missing **")
        elif classname not in storage.classes():
            print("** class doesn't exist **")
        elif uid is None:
            print("** instance id missing **")
        else:
            attributes = storage.attributes()[classname]
            for attribute, value in d.items():
                if attribute in attributes:
                    value = attributes[attribute](value)
                    setattr(storage.all()[key], attribute, value)
            storage.all()[key].save()

    def emptyline(self):
        """Nothing will happen in an Emptyline by hitting Enter."""
        pass

    def do_quit(self, line):
        """Type (quit) to exit the program."""
        return True

    def do_EOF(self, line):
        """Deals with EOF char."""
        print()
        return True

    def do_create(self, cln):
        """Create will create new instance."""
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
        Show details of an instance in JSON File.

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
        """Remove an Inst based on name & id of a class."""
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
                    del storage.all()[inst_id]
                    storage.save()

    def do_all(self, cln):
        """List all rep of all ins stored in Json."""
        if cln != "":
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

    def do_count(self, cln):
        """Count inst of the class."""
        command = cln.split(' ')
        if not command[0]:
            print("** class name missing **")
        elif command[0] not in storage.classes():
            print("** class doesn't exist **")
        else:
            alikes = [
                    key for key in storage.all() if key.startswith(
                        command[0] + '.')]
            print(len(alikes))

    def do_update(self, cln):
        """Update an instance."""
        if cln == "" or cln is None:
            print("** class name missing **")
            return

        regX = r'^(\S+)(?:\s(\S+)(?:\s(\S+)(?:\s((?:"[^"]*")|(?:(\S)+)))?)?)?'
        match = re.search(regX, cln)
        classname = match.group(1)
        uid = match.group(2)
        attribute = match.group(3)
        value = match.group(4)

        if not match:
            print("** class name missing **")
        elif classname not in storage.classes():
            print("** class doesn't exist **")
        elif uid is None:
            print("** instance id missing **")
        else:
            inst_key = "{}.{}".format(classname, uid)
            if inst_key not in storage.all():
                print("** no instance found **")
            elif not attribute:
                print("** attribute name missing **")
            elif not value:
                print("** value missing **")
            else:
                cast = None
                if not re.search('^".*"$', value):
                    if '.' in value:
                        cast = float
                    else:
                        cast = int
                else:
                    value = value.replace('"', '')
                attributes = storage.attributes()[classname]
                if attribute in attributes:
                    value = attributes[attribute](value)
                elif cast:
                    try:
                        value = cast(value)
                    except ValueError:
                        pass
                setattr(storage.all()[inst_key], attribute, value)
                storage.all()[inst_key].save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
