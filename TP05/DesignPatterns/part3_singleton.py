#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Workshop n°5 - Part 3: Singleton.

Test: the book's Singleton.
Q1. FileWriter: one single object, so one single access to the file in writing.
Q2. Database: one single object, so one single connection to the database (open, then close).
Q3. LimitedAccess: a limited number of simultaneous accesses (2 to the file, 3 to the database).
The files are created next to this script: journal.txt and shop.db.
"""
import os
import sqlite3
import threading

HERE = os.path.dirname(os.path.abspath(__file__))
TEXT_FILE = os.path.join(HERE, "journal.txt")
DB_FILE = os.path.join(HERE, "shop.db")


# ---------------------------------------------------------------- the book's code
class Singleton(object):
    instance = None                     # static attribute of the class

    def __new__(cls):
        """standard Python construction method"""
        if cls.instance is None:
            cls.instance = object.__new__(cls)
        return cls.instance


# ---------------------------------------------------------------- Q1
class FileWriter:
    """Opens the file once; every FileWriter() gives the same object and the same file."""
    _instance = None
    _lock = threading.Lock()            # also safe if two threads ask at the same moment

    def __new__(cls, filename=TEXT_FILE):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.filename = filename
                cls._instance.file = open(filename, "w", encoding="utf-8")
                print(f"  file opened for writing: {os.path.basename(filename)}")
        return cls._instance

    def write(self, text):
        self.file.write(text + "\n")
        self.file.flush()

    def close(self):
        self.file.close()
        FileWriter._instance = None     # the next FileWriter() may open the file again
        print("  file closed")


# ---------------------------------------------------------------- Q2
class Database:
    """One single connection to the database, opened by connect() and closed by close()."""
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, path=DB_FILE):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.path = path
                cls._instance.connection = None
        return cls._instance

    def connect(self):
        if self.connection is None:
            self.connection = sqlite3.connect(self.path)
            print(f"  connected to {os.path.basename(self.path)}")
        return self.connection

    def execute(self, sql, params=()):
        result = self.connect().execute(sql, params).fetchall()
        self.connection.commit()
        return result

    def close(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None
            print("  connection closed")


# ---------------------------------------------------------------- Q3
class LimitedAccess:
    """Like a singleton, but at most MAX_ACCESS objects can exist at the same time
    (a pool). A new access is refused until one of them is closed."""
    MAX_ACCESS = 1

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._open = 0                   # each kind of access has its own counter
        cls._lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._open >= cls.MAX_ACCESS:
                raise RuntimeError(f"{cls.__name__}: {cls.MAX_ACCESS} accesses already open, "
                                   "close one first")
            cls._open += 1
            obj = super().__new__(cls)
            obj.closed = False
            return obj

    def close(self):
        if not self.closed:
            self.closed = True
            with type(self)._lock:
                type(self)._open -= 1

    @classmethod
    def open_count(cls):
        return cls._open


class LimitedFileWriter(LimitedAccess):
    MAX_ACCESS = 2

    def __init__(self, user, filename=TEXT_FILE):
        self.user = user
        self.file = open(filename, "a", encoding="utf-8")

    def write(self, text):
        self.file.write(f"[{self.user}] {text}\n")
        self.file.flush()

    def close(self):
        if not self.closed:
            self.file.close()
        super().close()


class LimitedDatabase(LimitedAccess):
    MAX_ACCESS = 3

    def __init__(self, user, path=DB_FILE):
        self.user = user
        self.connection = sqlite3.connect(path)

    def close(self):
        if not self.closed:
            self.connection.close()
        super().close()


def try_open(kind, user):
    try:
        access = kind(user)
        print(f"  {user}: access granted ({kind.open_count()}/{kind.MAX_ACCESS} open)")
        return access
    except RuntimeError as error:
        print(f"  {user}: REFUSED - {error}")
        return None


if __name__ == "__main__":
    print("===== Test of the book's Singleton =====")
    monSingleton1 = Singleton()
    monSingleton2 = Singleton()
    assert monSingleton1 is monSingleton2       # they return the same instance
    print(" ", monSingleton1, monSingleton2)
    print("  same instance:", monSingleton1 is monSingleton2)

    print("\n===== Q1: unique access to a file in writing =====")
    writer1 = FileWriter()
    writer2 = FileWriter("another_file.txt")    # no new file: the same object is returned
    print("  writer1 is writer2:", writer1 is writer2, "| same file:", writer1.file is writer2.file)
    writer1.write("line written by writer1")
    writer2.write("line written by writer2")
    writer1.close()
    with open(TEXT_FILE, encoding="utf-8") as f:
        print("  content of journal.txt:", f.read().splitlines())

    print("\n===== Q2: unique access to the database =====")
    db1 = Database()
    db2 = Database()
    print("  db1 is db2:", db1 is db2)
    print("  same connection:", db1.connect() is db2.connect())
    db1.execute("DROP TABLE IF EXISTS products")
    db1.execute("CREATE TABLE products (name TEXT, qty INTEGER)")
    db2.execute("INSERT INTO products VALUES (?, ?)", ("Laptop", 5))
    print("  read through db1 what db2 wrote:", db1.execute("SELECT * FROM products"))
    db2.close()
    print("  db1 is also closed:", db1.connection is None)

    print("\n===== Q3: limited number of simultaneous accesses =====")
    print(f"  file: at most {LimitedFileWriter.MAX_ACCESS} writers at the same time")
    a = try_open(LimitedFileWriter, "Ahmed")
    b = try_open(LimitedFileWriter, "Sara")
    c = try_open(LimitedFileWriter, "Karim")    # third one: refused
    a.write("hello")
    a.close()
    print("  Ahmed closed his access")
    c = try_open(LimitedFileWriter, "Karim")    # now there is a free place
    b.close()
    c.close()

    print(f"\n  database: at most {LimitedDatabase.MAX_ACCESS} connections at the same time")
    users = [try_open(LimitedDatabase, name) for name in ("App", "Admin", "Report", "Backup")]
    users[0].close()
    print("  App closed its connection")
    users[3] = try_open(LimitedDatabase, "Backup")
    for user in users[1:]:
        user.close()
    print("  all closed, open accesses:", LimitedDatabase.open_count())
