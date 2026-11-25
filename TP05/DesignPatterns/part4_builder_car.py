#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Workshop n°5 - Part 4, Question 3: cars sold with several options, built according to orders.

Car          : the product
CarBuilder   : abstract builder - one method per part (engine, gearbox, each option)
ConcreteCarBuilder : builds the Car object
QuoteBuilder       : follows the SAME steps but builds the price quote for the customer
CarDealer    : director - the basic car, the full car, or a car built from an order
Prices are in Algerian dinars (DA).
"""
from abc import ABC, abstractmethod

BASE_PRICE = 2_900_000
OPTIONS = {                       # option name -> (description, price)
    "air_conditioning": ("Air conditioning", 120_000),
    "gps": ("GPS navigation", 80_000),
    "rear_camera": ("Rear camera", 60_000),
    "leather_seats": ("Leather seats", 150_000),
    "sunroof": ("Sunroof", 180_000),
    "alloy_wheels": ("Alloy wheels", 90_000),
}
ENGINES = {"1.2 petrol": 0, "1.6 diesel": 350_000}
GEARBOXES = {"manual": 0, "automatic": 250_000}


class Car:
    """The product."""

    def __init__(self, model):
        self.model = model
        self.engine = None
        self.gearbox = None
        self.options = []

    def show(self):
        print(f"  {self.model}: {self.engine} engine, {self.gearbox} gearbox")
        print(f"    options: {', '.join(self.options) or 'none'}")


class CarBuilder(ABC):
    """Abstract builder."""

    @abstractmethod
    def reset(self, model): ...

    @abstractmethod
    def set_engine(self, engine): ...

    @abstractmethod
    def set_gearbox(self, gearbox): ...

    @abstractmethod
    def add_option(self, option): ...

    @abstractmethod
    def get_result(self): ...


class ConcreteCarBuilder(CarBuilder):
    def reset(self, model):
        self._car = Car(model)

    def set_engine(self, engine):
        self._car.engine = engine

    def set_gearbox(self, gearbox):
        self._car.gearbox = gearbox

    def add_option(self, option):
        self._car.options.append(OPTIONS[option][0])

    def get_result(self):
        return self._car


class QuoteBuilder(CarBuilder):
    """Another representation built by the same steps: the price quote."""

    def reset(self, model):
        self._lines = [(f"{model} (base)", BASE_PRICE)]

    def set_engine(self, engine):
        self._lines.append((f"Engine {engine}", ENGINES[engine]))

    def set_gearbox(self, gearbox):
        self._lines.append((f"Gearbox {gearbox}", GEARBOXES[gearbox]))

    def add_option(self, option):
        self._lines.append(OPTIONS[option])

    def get_result(self):
        total = sum(price for _, price in self._lines)
        text = [f"    {name:<22}{price:>12,} DA" for name, price in self._lines]
        text.append(f"    {'TOTAL':<22}{total:>12,} DA")
        return "\n".join(text)


class CarDealer:
    """Director: knows the versions sold and builds a car from an order."""
    MODEL = "Atlas"

    def basic(self, builder):
        """The basic version: no option."""
        return self.order(builder, engine="1.2 petrol", gearbox="manual", options=[])

    def full(self, builder):
        """The whole version: the strongest engine and every option."""
        return self.order(builder, engine="1.6 diesel", gearbox="automatic", options=list(OPTIONS))

    def order(self, builder, engine="1.2 petrol", gearbox="manual", options=()):
        """A car with or without some options, as the customer ordered it."""
        unknown = [o for o in options if o not in OPTIONS]
        if unknown:
            raise ValueError(f"unknown options: {unknown}")
        builder.reset(self.MODEL)
        builder.set_engine(engine)
        builder.set_gearbox(gearbox)
        for option in options:
            builder.add_option(option)
        return builder.get_result()


if __name__ == "__main__":
    dealer = CarDealer()
    orders = {
        "Basic version": dict(),
        "Full version": None,
        "Order of a customer: basic + air conditioning + rear camera":
            dict(options=["air_conditioning", "rear_camera"]),
        "Order of a customer: diesel, automatic, GPS, no other option":
            dict(engine="1.6 diesel", gearbox="automatic", options=["gps"]),
    }
    for title, order in orders.items():
        print(f"===== {title} =====")
        if order is None:
            car, quote = dealer.full(ConcreteCarBuilder()), dealer.full(QuoteBuilder())
        elif not order:
            car, quote = dealer.basic(ConcreteCarBuilder()), dealer.basic(QuoteBuilder())
        else:
            car, quote = dealer.order(ConcreteCarBuilder(), **order), dealer.order(QuoteBuilder(), **order)
        car.show()
        print(quote)
        print()
