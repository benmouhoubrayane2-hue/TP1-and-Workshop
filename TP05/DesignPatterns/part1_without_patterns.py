#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Workshop n°5 - Part 1: without design patterns.

The client creates the objects itself with if/elif: to add a shape (Q2), this
code must be modified, and every other place that creates shapes too.
Fixed from the book: Shape was not defined; print "..." is Python 2 syntax.
"""
import sys

from shapes import Circle, Square, Triangle, Rectangle


def run(types):
    for type in types:
        if type == "Circle":
            shape = Circle()
        elif type == "Square":
            shape = Square()
        elif type == "Triangle":             # Q2
            shape = Triangle()
        elif type == "Rectangle":            # Q2
            shape = Rectangle()
        else:
            print("Bad shape creation: " + type)
            sys.exit()
        shape.draw()
        shape.erase()


if __name__ == "__main__":
    print("===== Q1: run the program =====")
    run(("Circle", "Square", "Circle", "Square"))

    print("\n===== Q2: triangle and rectangle added =====")
    run(("Circle", "Square", "Triangle", "Rectangle"))
