#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Workshop n°5 - Part 4, Questions 1 and 2: sandwiches built with the Builder pattern.

Q1. Each configuration of the sandwich has a name: it is a method of the director
    (SandwichChef): shawarma(), ground_meat(), fried_omelet(), tuna() ...
Q2. The product (Sandwich) is created step by step by a builder; two concrete builders
    give two representations of the same recipe: in a baguette or rolled in a wrap.
Prices are in Algerian dinars (DA).
"""
from abc import ABC, abstractmethod


class Sandwich:
    """The product."""

    def __init__(self):
        self.name = "Custom sandwich"
        self.bread = None
        self.fillings = []
        self.sauces = []
        self.price = 0

    def show(self):
        print(f"  {self.name} - {self.bread}")
        print(f"    fillings: {', '.join(self.fillings)}")
        print(f"    sauces  : {', '.join(self.sauces) or 'none'}")
        print(f"    price   : {self.price} DA")


class SandwichBuilder(ABC):
    """Abstract builder: one method per part of the sandwich."""
    PRICES = {"chicken shawarma": 250, "ground meat": 220, "fried potatoes": 60, "omelet": 70,
              "tuna": 150, "cheese": 60, "tomato": 20, "onion": 10, "salad": 20, "olives": 30,
              "pickles": 20, "boiled egg": 30}

    def __init__(self):
        self.reset()

    def reset(self):
        self._sandwich = Sandwich()
        self._sandwich.bread, self._sandwich.price = self.bread()

    @abstractmethod
    def bread(self):
        """(name, price) of the bread of this kind of sandwich."""

    def set_name(self, name):
        self._sandwich.name = name
        return self

    def add_filling(self, *items):
        for item in items:
            self._sandwich.fillings.append(item)
            self._sandwich.price += self.PRICES.get(item, 30)
        return self

    def add_sauce(self, *sauces):
        self._sandwich.sauces.extend(sauces)
        return self

    def get_sandwich(self):
        """Give the finished sandwich and start a new one."""
        sandwich = self._sandwich
        self.reset()
        return sandwich


class BaguetteBuilder(SandwichBuilder):
    def bread(self):
        return "in a baguette", 40


class WrapBuilder(SandwichBuilder):
    def bread(self):
        return "rolled in a wrap (galette)", 60


class SandwichChef:
    """Director: the named configurations (Q1)."""

    def __init__(self, builder):
        self.builder = builder

    def shawarma(self):
        return (self.builder.set_name("Shawarma sandwich")
                .add_filling("chicken shawarma", "fried potatoes", "pickles", "tomato")
                .add_sauce("garlic sauce").get_sandwich())

    def ground_meat(self):
        return (self.builder.set_name("Ground meat sandwich")
                .add_filling("ground meat", "onion", "tomato", "salad")
                .add_sauce("harissa").get_sandwich())

    def fried_omelet(self):
        return (self.builder.set_name("Fried potatoes with omelet")
                .add_filling("fried potatoes", "omelet", "cheese")
                .add_sauce("mayonnaise", "ketchup").get_sandwich())

    def tuna(self):                                     # "Etc."
        return (self.builder.set_name("Tuna sandwich")
                .add_filling("tuna", "boiled egg", "olives", "salad")
                .add_sauce("harissa").get_sandwich())


if __name__ == "__main__":
    print("===== Q1/Q2: named configurations, in a baguette =====")
    chef = SandwichChef(BaguetteBuilder())
    for order in (chef.shawarma, chef.ground_meat, chef.fried_omelet, chef.tuna):
        order().show()

    print("\n===== Same configurations, another builder: in a wrap =====")
    chef = SandwichChef(WrapBuilder())
    chef.shawarma().show()
    chef.fried_omelet().show()

    print("\n===== A sandwich made step by step by the customer (no director) =====")
    custom = (BaguetteBuilder().set_name("My sandwich")
              .add_filling("ground meat", "cheese", "fried potatoes")
              .add_sauce("mayonnaise").get_sandwich())
    custom.show()
