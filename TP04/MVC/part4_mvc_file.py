#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Workshop n°4 - Part 4: same view and controller, the model now stores the data in a file.
from model_file import model_file
from part3_mvc_class import view, controller

if __name__ == '__main__':
    # Q2: the main program only changes the model given to the controller
    contro = controller(model_file(), view())

    print("===== Part 4: directory loaded from directory.txt =====")
    contro.get_all()

    print("\n===== Part 4: search =====")
    contro.search()

    print("\n===== Part 4: add a person (saved in directory.txt) =====")
    contro.add()
