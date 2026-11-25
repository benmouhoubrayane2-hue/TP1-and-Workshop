#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Workshop n°5 - the shapes used in Part 1.

The book's code uses a class Shape that is never defined (NameError): it is defined here.
Triangle and Rectangle answer Part 1, question 2 ("add a triangle and rectangle shape").
"""


class Shape:
    """Base class of every shape."""

    def draw(self):
        raise NotImplementedError

    def erase(self):
        raise NotImplementedError


class Circle(Shape):
    def draw(self): print("Circle.draw")
    def erase(self): print("Circle.erase")


class Square(Shape):
    def draw(self): print("Square.draw")
    def erase(self): print("Square.erase")


class Triangle(Shape):                       # Q2: new shape
    def draw(self): print("Triangle.draw")
    def erase(self): print("Triangle.erase")


class Rectangle(Shape):                      # Q2: new shape
    def draw(self): print("Rectangle.draw")
    def erase(self): print("Rectangle.erase")
