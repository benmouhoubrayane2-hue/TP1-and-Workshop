#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Workshop n°4 - Part 2 Q6 (controller CLASS) and Part 3 (adding people).


class model:
    """ data model class """

    def __init__(self):
        self.directory = [
            {"firstname": 'Ahmed',   "familyname": 'Mahdi',   'tel': '0778787887'},
            {"firstname": 'Mohamed', "familyname": 'Mahdi',   'tel': '0778787887'},
            {"firstname": 'Mounir',  "familyname": 'Katibi',  'tel': '0778787887'},
            {"firstname": 'Noui',    "familyname": 'Brahimi', 'tel': '0778787887'},
        ]

    def search(self, name):
        """ lookup for a tel by family name """
        return [persn for persn in self.directory if persn["familyname"] == name]

    def get_all(self):
        """ every person of the directory """
        return list(self.directory)

    def add(self, name, firstname, tel):
        """ Part 3: add a person """
        person = {}
        person["familyname"] = name
        person["firstname"] = firstname
        person["tel"] = tel
        self.directory.append(person)


class view:
    """ console view """

    def input(self):
        """ retrieve the name to search for """
        print("Finding a phone")
        print("Give a name")
        return input()

    def input_add(self):
        """ Part 3: get the person to add """
        print("Add a person")
        print("Give a name")
        name = input()
        print("Give a firstname")
        firstname = input()
        print("Give a phone number")      # the book asked "Give a firstname" twice
        tel = input()
        return (name, firstname, tel)

    def input_count(self):
        """ Part 3 Q3: how many people to add """
        while True:
            print("How many people do you want to add?")
            answer = input()
            if answer.strip().isdigit():
                return int(answer)
            print("Please type a whole number.")

    def output(self, persons):
        """ display information from a list of persons """
        print("List of found names")
        print(" %d found people " % len(persons))
        for pers in persons:
            print(pers["familyname"], pers["firstname"], pers['tel'])


class controller:
    """ Q6: the controller is now a class (one method per user action) """

    def __init__(self, data_model=None, viewer=None):
        """ controller constructor: the model and the view can be given (used in Part 4) """
        self.data_model = data_model if data_model is not None else model()
        self.viewer = viewer if viewer is not None else view()

    def search(self):
        """ search a name """
        name = self.viewer.input()
        persons = self.data_model.search(name)
        self.viewer.output(persons)

    def get_all(self):
        """ display all people """
        self.viewer.output(self.data_model.get_all())

    def add(self):
        """ Part 3: add a new person, then display the directory """
        name, firstname, tel = self.viewer.input_add()
        self.data_model.add(name, firstname, tel)
        persons = self.data_model.get_all()
        self.viewer.output(persons)

    def add_many(self):
        """ Part 3 Q3: add several people, then display the directory """
        count = self.viewer.input_count()
        for _ in range(count):
            name, firstname, tel = self.viewer.input_add()
            self.data_model.add(name, firstname, tel)
        self.viewer.output(self.data_model.get_all())


if __name__ == '__main__':
    contro = controller()

    print("===== Part 2 Q6: search with the controller class =====")
    contro.search()

    print("\n===== Part 3 Q2: add one person =====")
    contro.add()

    print("\n===== Part 3 Q3: add several people =====")
    contro.add_many()
