#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Workshop n°5 - Part 1, Application: stock management with three kinds of accounts.

Q1. Pattern: FACTORY METHOD (taken from the class diagram). The client never writes
    Gestionnaire(...), Vendeur(...) or Visiteur(...): it asks the factory
    (CompteFactory.createCompte) for the account it needs.
Q2. Base classes (Compte and its three subclasses) and the creation classes
    (CompteFactory, ConcreteCompteFactory).
"""
from abc import ABC, abstractmethod


class Store:
    """The shop's data, shared by every account."""

    def __init__(self):
        self.products = {"Laptop": (5, 85000), "Mouse": (20, 1500), "Keyboard": (8, 3500)}  # name: (qty, price DA)
        self.incomes = 0
        self.orders = []


# ----------------------------------------------------------------- products
class Compte(ABC):
    """An account of the application: every account can see the stock, buy and order."""
    ROLE = "account"

    def __init__(self, name, store):
        self.name = name
        self.store = store

    def __str__(self):
        return f"{self.ROLE} '{self.name}'"

    def stock(self):
        """See the stock."""
        print(f"  [{self}] stock:", ", ".join(f"{p} x{q}" for p, (q, _) in self.store.products.items()))

    def _take(self, product, qty):
        """Remove `qty` products from the stock and cash the money; None if not enough."""
        stock, price = self.store.products[product]
        if qty > stock:
            print(f"  [{self}] refused: only {stock} {product} left")
            return None
        self.store.products[product] = (stock - qty, price)
        self.store.incomes += qty * price
        return qty * price

    def achat(self, product, qty):
        """Make a purchase: the stock goes down and the shop earns money."""
        amount = self._take(product, qty)
        if amount is not None:
            print(f"  [{self}] bought {qty} {product} ({amount} DA)")
        return amount is not None

    def commande(self, product, qty):
        """Place an order (delivered later)."""
        self.store.orders.append((self.name, product, qty))
        print(f"  [{self}] ordered {qty} {product}")


class Gestionnaire(Compte):
    """Manager: manages the stock, buys, orders and sees the total incomes."""
    ROLE = "manager"

    def gerer_stock(self, product, qty, price=None):
        old_qty, old_price = self.store.products.get(product, (0, price))
        self.store.products[product] = (old_qty + qty, price or old_price)
        print(f"  [{self}] added {qty} {product} to the stock")

    def revenus(self):
        print(f"  [{self}] total incomes: {self.store.incomes} DA, orders: {len(self.store.orders)}")
        return self.store.incomes


class Vendeur(Compte):
    """Seller: sells to customers, buys and orders."""
    ROLE = "seller"

    def vente(self, customer, product, qty):
        amount = self._take(product, qty)
        if amount is not None:
            print(f"  [{self}] sold {qty} {product} to {customer} ({amount} DA)")
        return amount is not None


class Visiteur(Compte):
    """Visitor (customer): sees the stock, buys and orders - nothing more."""
    ROLE = "visitor"


# ----------------------------------------------------------------- creators
class CompteFactory(ABC):
    """Creator: declares the factory method."""

    @abstractmethod
    def createCompte(self, kind, name, store):
        """FACTORY METHOD: return a new account of the kind asked for."""


class ConcreteCompteFactory(CompteFactory):
    ACCOUNTS = {"manager": Gestionnaire, "seller": Vendeur, "visitor": Visiteur}

    def createCompte(self, kind, name, store):
        if kind not in self.ACCOUNTS:
            raise ValueError(f"unknown account type: {kind}")
        return self.ACCOUNTS[kind](name, store)


if __name__ == "__main__":
    store = Store()
    factory = ConcreteCompteFactory()                       # the client only knows the factory

    print("===== Q2: accounts created by the factory =====")
    manager = factory.createCompte("manager", "Karim", store)
    seller = factory.createCompte("seller", "Sara", store)
    visitor = factory.createCompte("visitor", "Yacine", store)
    for account in (manager, seller, visitor):
        print(f"  {account} -> {account.__class__.__name__}")

    print("\n===== Visitor: see the stock, buy, order =====")
    visitor.stock()
    visitor.achat("Mouse", 2)
    visitor.commande("Laptop", 1)
    visitor.achat("Keyboard", 50)                      # more than the stock

    print("\n===== Seller: sell, buy, order =====")
    seller.vente("a customer", "Keyboard", 3)
    seller.achat("Laptop", 1)
    seller.commande("Mouse", 10)

    print("\n===== Manager: manage the stock, see the total incomes =====")
    manager.gerer_stock("Laptop", 3)
    manager.stock()
    manager.revenus()

    print("\n===== Rights of each account =====")
    for account in (manager, seller, visitor):
        rights = [m for m in ("stock", "achat", "commande", "vente", "gerer_stock", "revenus")
                  if hasattr(account, m)]
        print(f"  {account.ROLE:8}: {', '.join(rights)}")
