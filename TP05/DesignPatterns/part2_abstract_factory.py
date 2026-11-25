#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Workshop n°5 - Part 2: Abstract Factory - 2D shapes and 3D shapes.

1. Subclasses Circle2D, Circle3D, Square2D, Square3D.
2. The abstract factory ShapeFactory.
3. The concrete factories ShapeFactory2D and ShapeFactory3D.
4. Examples: the same client code creates a 2D family or a 3D family,
   depending only on the factory it is given.
"""
from abc import ABC, abstractmethod


class Shape(ABC):
    @abstractmethod
    def draw(self): ...

    @abstractmethod
    def erase(self): ...


class Circle(Shape, ABC):
    pass


class Square(Shape, ABC):
    pass


# 1. the four subclasses
class Circle2D(Circle):
    def draw(self): print("Circle.draw2D")
    def erase(self): print("Circle.erase2D")


class Circle3D(Circle):
    def draw(self): print("Circle.draw3D")
    def erase(self): print("Circle.erase3D")


class Square2D(Square):
    def draw(self): print("Square.draw2D")
    def erase(self): print("Square.erase2D")


class Square3D(Square):
    def draw(self): print("Square.draw3D")
    def erase(self): print("Square.erase3D")


# 2. the abstract factory
class ShapeFactory(ABC):
    @staticmethod
    @abstractmethod
    def createShape(type):
        """Return a Circle or a Square of the factory's family."""


# 3. the concrete factories
class ShapeFactory2D(ShapeFactory):
    @staticmethod
    def createShape(type):
        if type == "Circle":
            return Circle2D()
        elif type == "Square":
            return Square2D()
        else:
            return None


class ShapeFactory3D(ShapeFactory):
    @staticmethod
    def createShape(type):
        if type == "Circle":
            return Circle3D()
        elif type == "Square":
            return Square3D()
        else:
            return None


def draw_scene(factory):
    """Client code: it only knows the abstract factory and the abstract shapes."""
    for type in ("Circle", "Square", "Circle", "Square"):
        shape = factory.createShape(type)
        shape.draw()
        shape.erase()


# 4. examples
if __name__ == "__main__":
    print("===== 2D objects creation =====")
    draw_scene(ShapeFactory2D)

    print("\n===== 3D objects creation =====")
    draw_scene(ShapeFactory3D)

    print("\n===== Checks =====")
    print("Circle3D is a Circle and a Shape:", isinstance(Circle3D(), Circle) and isinstance(Circle3D(), Shape))
    print("ShapeFactory2D never mixes in 3D:", all(type(ShapeFactory2D.createShape(t)).__name__.endswith("2D")
                                                    for t in ("Circle", "Square")))
    try:
        ShapeFactory()
    except TypeError:
        print("ShapeFactory is abstract: it cannot be instantiated")
