#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Workshop n°5 - Part 1: Factory Method.

ShapeFactory is the creator: produce() is written once and calls the factory
method create_shape(), which each specialised factory implements in its own way:
  - ShapeFactory_SCT produces only Squares, Circles and Triangles;
  - ShapeFactory_SCR produces only Squares, Circles and Rectangles.
"""
from abc import ABC, abstractmethod

from shapes import Circle, Square, Triangle, Rectangle


class ShapeFactory(ABC):
    """Creator."""

    def produce(self, kind):
        """Common to every factory: create the shape, then draw and erase it."""
        shape = self.create_shape(kind)
        if shape is None:
            print(f"{self.__class__.__name__} does not produce a {kind}")
            return None
        shape.draw()
        shape.erase()
        return shape

    @abstractmethod
    def create_shape(self, kind):
        """FACTORY METHOD: return a new shape, or None if this factory does not make it."""


class ShapeFactory_SCT(ShapeFactory):
    """Squares, Circles and Triangles."""

    def create_shape(self, kind):
        products = {"Square": Square, "Circle": Circle, "Triangle": Triangle}
        return products[kind]() if kind in products else None


class ShapeFactory_SCR(ShapeFactory):
    """Squares, Circles and Rectangles."""

    def create_shape(self, kind):
        products = {"Square": Square, "Circle": Circle, "Rectangle": Rectangle}
        return products[kind]() if kind in products else None


if __name__ == "__main__":
    orders = ("Square", "Circle", "Triangle", "Rectangle")
    for factory in (ShapeFactory_SCT(), ShapeFactory_SCR()):
        print(f"===== {factory.__class__.__name__} =====")
        for kind in orders:
            factory.produce(kind)
        print()
