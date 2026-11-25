#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Workshop n°5 - Part 1: Simple Factory.

Q1: the object creation is encapsulated in ShapeFactory.createShape(); the client
only asks for a shape by its name.
Q2: adding the triangle and the rectangle only changes the factory, not the client.
"""
import sys

from shapes import Circle, Square, Triangle, Rectangle


class ShapeFactory:
    @staticmethod
    def createShape(type):
        if type == "Circle":
            return Circle()
        elif type == "Square":
            return Square()
        elif type == "Triangle":             # Q2
            return Triangle()
        elif type == "Rectangle":            # Q2
            return Rectangle()
        else:
            print("Bad shape creation: " + type)
            sys.exit()


def run(types):
    for type in types:
        shape = ShapeFactory.createShape(type)
        shape.draw()
        shape.erase()


if __name__ == "__main__":
    print("===== Q1: creation through ShapeFactory =====")
    run(("Circle", "Square", "Circle", "Square"))

    print("\n===== Q2: triangle and rectangle added (only the factory changed) =====")
    run(("Circle", "Square", "Triangle", "Rectangle"))
