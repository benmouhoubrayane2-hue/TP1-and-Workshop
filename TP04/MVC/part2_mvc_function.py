#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Workshop n°4 - Part 2 (Q1 to Q5): model and view classes, controller FUNCTION.


class model:
    """ data model class: holds the data and searches it (never prints) """

    def __init__(self):
        self.directory = [
            {"firstname": 'Ahmed',   "familyname": 'Mahdi',   'tel': '0778787887'},
            {"firstname": 'Mohamed', "familyname": 'Mahdi',   'tel': '0778787887'},
            {"firstname": 'Mounir',  "familyname": 'Katibi',  'tel': '0778787887'},
            {"firstname": 'Noui',    "familyname": 'Brahimi', 'tel': '0778787887'},
        ]

    def search(self, name):
        """ lookup for a tel by family name """
        persons = []
        for persn in self.directory:
            if persn["familyname"] == name:
                persons.append(persn)
        return persons                  # a list of dictionaries

    def get_all(self):
        """ Q3: return every person of the directory """
        persons = []
        for persn in self.directory:
            persons.append(persn)
        return persons


class view:
    """ display class: reads the keyboard and prints (never searches) """

    def __init__(self):
        pass

    def input(self):
        """ retrieve the name to search for """
        print("Finding a phone")
        print("Give a name")
        name = input()
        return name

    def output(self, persons):
        """ display information from a list of persons """
        print("List of found names")
        print(" %d found people " % len(persons))
        for pers in persons:
            print(pers["familyname"], pers["firstname"], pers['tel'])


def controller():
    """ links the model and the view """
    data_model = model()
    my_viewer = view()

    # search a name
    name = my_viewer.input()
    persons = data_model.search(name)
    my_viewer.output(persons)

    # Q4: display all people (the view is reused unchanged - Q5)
    print()
    persons = data_model.get_all()
    my_viewer.output(persons)


if __name__ == '__main__':
    controller()
