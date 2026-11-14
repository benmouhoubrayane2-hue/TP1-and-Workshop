#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Workshop n°4 - Part 4: a data model that stores the directory in a text file.
# Fields separated by tabs: family name, first name, phone.
import os
import sys

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "directory.txt")


class model_file:
    """ Data Model class: same methods as "model", but the data lives in a file """

    def __init__(self, filename=DATA_FILE):
        self.filename = filename
        self.directory = []
        try:
            myfile = open(self.filename, encoding="utf-8")
        except OSError:
            print("Can't open DataFile")
            sys.exit()
        lines = myfile.readlines()
        for line in lines:
            line = line.strip('\n')
            if not line.strip():          # skip empty lines
                continue
            fields = line.split('\t')
            person = {}
            person["familyname"] = fields[0]
            person["firstname"] = fields[1]  # the book wrote "lastname" here
            person["tel"] = fields[2]
            self.directory.append(person)
        myfile.close()

    def save(self):
        """ write the whole directory back to the file """
        try:
            myfile = open(self.filename, "w", encoding="utf-8")
        except OSError:
            print("Can't open DataFile")
            sys.exit()
        for person in self.directory:
            line = "\t".join([person['familyname'],
                              person['firstname'],
                              person['tel'],
                              ])
            line += "\n"
            myfile.write(line)
        myfile.close()

    def __del__(self):
        """ Destructor of the Model class: saves the data at the end of the program """
        try:
            self.save()
        except Exception:
            pass

    # The following methods are identical to the methods of the "model" class.
    def search(self, name):
        return [persn for persn in self.directory if persn["familyname"] == name]

    def get_all(self):
        return list(self.directory)

    def add(self, name, firstname, tel):
        person = {"familyname": name, "firstname": firstname, "tel": tel}
        self.directory.append(person)
        self.save()                       # saved at once, not only in __del__
