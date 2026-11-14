#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Workshop n°4 - Part 5: MVC + graphical interface (same model_file as Part 4).
from model_file import model_file
from view_tk import view_tk


def controller3():
    data_model = model_file()
    my_viewer = view_tk(data_model)
    my_viewer.run()  # launch GUI


if __name__ == '__main__':
    controller3()
