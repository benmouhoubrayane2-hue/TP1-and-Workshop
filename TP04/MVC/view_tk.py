#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Workshop n°4 - Part 5: a graphical view (Tkinter) for the same file model.
from tkinter import Tk, Label, Button, Text, END, W, E


class view_tk:

    def __init__(self, model):
        master = Tk()
        self.master = master
        self.model = model
        master.title("Directory")

        self.label = Label(master, text="Family name:")
        self.entry = Text(master, height=1, width=20)
        self.label_firstname = Label(master, text="First Name:")
        self.entry_firstname = Text(master, height=1, width=20)
        self.label_tel = Label(master, text="Tel:")
        self.entry_tel = Text(master, height=1, width=20)
        self.output_label = Label(master, text="Output")
        self.output = Text(master, height=10, width=64)

        self.search_button = Button(master, text="Search",
                                    command=lambda: self.update("search"))
        self.add_button = Button(master, text="Add",
                                 command=lambda: self.update("add"))
        self.all_button = Button(master, text="Get All",
                                 command=lambda: self.update("get_all"))

        # LAYOUT: one column per field (the book's columnspan=10 made the fields overlap)
        self.label.grid(row=0, column=0, sticky=W, padx=4)
        self.label_firstname.grid(row=0, column=1, sticky=W, padx=4)
        self.label_tel.grid(row=0, column=2, sticky=W, padx=4)
        self.entry.grid(row=1, column=0, sticky=W + E, padx=4)
        self.entry_firstname.grid(row=1, column=1, sticky=W + E, padx=4)
        self.entry_tel.grid(row=1, column=2, sticky=W + E, padx=4)
        self.search_button.grid(row=2, column=0, pady=6)
        self.add_button.grid(row=2, column=1, pady=6)
        self.all_button.grid(row=2, column=2, pady=6)
        self.output_label.grid(row=3, column=0, sticky=W, padx=4)
        self.output.grid(row=4, column=0, columnspan=3, sticky=W + E, padx=4, pady=(0, 6))

    def update(self, method):
        familyname = self.entry.get("1.0", END).strip()
        firstname = self.entry_firstname.get("1.0", END).strip()   # book read entry_tel
        tel = self.entry_tel.get("1.0", END).strip()

        if method == "search":
            result = self.search(familyname)
        elif method == "add":
            result = self.add(familyname, firstname, tel)
        elif method == "get_all":
            result = self.get_all()
        else:  # reset
            result = familyname

        self.output.delete("1.0", END)          # show only the latest result
        self.output.insert(END, result)

    @staticmethod
    def format(persons):
        """ one readable line per person instead of a raw Python list """
        lines = ["%d found people" % len(persons)]
        for p in persons:
            lines.append("%-12s %-12s %s" % (p["familyname"], p["firstname"], p["tel"]))
        return "\n".join(lines)

    def add(self, familyname, firstname, tel):
        if not (familyname and firstname and tel):
            return "Fill in the family name, the first name and the phone."
        self.model.add(familyname, firstname, tel)              # book: model.ajouter
        return "Added: %s %s %s\n\n" % (familyname, firstname, tel) + self.get_all()

    def search(self, familyname):
        result = self.model.search(familyname)                  # book: model.rechercher
        if result:
            return self.format(result)
        else:
            return "'%s' not found" % familyname

    def get_all(self):
        return self.format(self.model.get_all())

    def run(self):
        self.master.mainloop()
