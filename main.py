from abc import ABC, abstractmethod


# ==========================================
# 1. Single Responsibility Principle (SRP)
# ==========================================
class Order:
    def __init__(self, items):
        self.items = items

    def calculate_total(self):
        return sum(item['price'] for item in self.items)


class OrderPrinter:
    def print_order(self, order):
        print("Order details:")
        for item in order.items:
            print(f"- {item['name']}: ${item['price']}")


class OrderRepository:
    def save_to_db(self, order):
        print("Saving order to database...")


# ==========================================
# 2. Open/Closed Principle (OCP)
# ==========================================
class Discount:
    def __init__(self, price):
        self.price = price

    def apply_discount(self):
        return self.price


class VIPDiscount(Discount):
    def apply_discount(self):
        return self.price * 0.8  # 20% discount


class FirstTimeDiscount(Discount):
    def apply_discount(self):
        return self.price * 0.85  # 15% discount


# ==========================================
# 3. Liskov Substitution Principle (LSP)
# ==========================================
class Shape(ABC):
    @abstractmethod
    def get_area(self):
        pass


class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def get_area(self):
        return self.width * self.height


class Square(Shape):
    def __init__(self, side_length):
        self.side_length = side_length

    def get_area(self):
        return self.side_length ** 2


def print_area(shape: Shape):
    print(f"Shape area ({shape.__class__.__name__}): {shape.get_area()}")


# Solution for the Person / Student / Employee scenario
class Person:
    def __init__(self, name, email):
        self.name = name
        self.email = email


class Employee(Person):
    def __init__(self, name, email, salary):
        super().__init__(name, email)
        self.salary = salary

    def get_salary(self):
        return self.salary

    def assign_task(self, task):
        print(f"Task '{task}' assigned to employee {self.name}.")


class Student(Person):
    def __init__(self, name, email, student_id):
        super().__init__(name, email)
        self.student_id = student_id


# ==========================================
# 4. Interface Segregation Principle (ISP)
# ==========================================
# Interfaces for the printing system
class Printable(ABC):
    @abstractmethod
    def print_document(self, document):
        pass


class Scannable(ABC):
    @abstractmethod
    def scan_document(self, document):
        pass


class Faxable(ABC):
    @abstractmethod
    def fax_document(self, document):
        pass


# Printer implementations
class BasicPrinter(Printable):
    def print_document(self, document):
        print(f"Printing: {document}")


class AdvancedPrinter(Printable, Scannable, Faxable):
    def print_document(self, document):
        print(f"Printing: {document}")

    def scan_document(self, document):
        print(f"Scanning: {document}")

    def fax_document(self, document):
        print(f"Faxing: {document}")


# Interfaces for academic roles
class Teacher(ABC):
    @abstractmethod
    def teach(self):
        pass


class Researcher(ABC):
    @abstractmethod
    def research(self):
        pass


class Doctor(ABC):
    @abstractmethod
    def practice_medicine(self):
        pass


# Academic classes: each one implements only the interfaces of its own tasks
class ProfessorResearcher(Teacher, Researcher):
    def teach(self):
        print("Teaches courses to students.")

    def research(self):
        print("Conducts scientific research.")


class FullTimeResearcher(Researcher):  # does not teach: no teach() method at all
    def research(self):
        print("Exclusively performs research work.")


class ProfessorHospitalResearcher(Teacher, Researcher, Doctor):
    def teach(self):
        print("Teaches medicine to students.")

    def research(self):
        print("Conducts medical research.")

    def practice_medicine(self):
        print("Practices medicine at the hospital.")


# ==========================================
# 5. Dependency Inversion Principle (DIP)
# ==========================================
# Notification Service
class NotificationService(ABC):
    @abstractmethod
    def send(self, message):
        pass


class EmailService(NotificationService):
    def send(self, message):
        print(f"Sending Email: {message}")


class SMSService(NotificationService):
    def send(self, message):
        print(f"Sending SMS: {message}")


class PushNotificationService(NotificationService):
    def send(self, message):
        print(f"Sending Push Notification: {message}")


class Notification:
    def __init__(self, service: NotificationService):
        self.service = service

    def send(self, message):
        self.service.send(message)


# Refactoring Application & Logger
class ILogger(ABC):
    @abstractmethod
    def log(self, message):
        pass


class FileLogger(ILogger):
    def log(self, message):
        print(f"Logging to file: {message}")


class DatabaseLogger(ILogger):
    def log(self, message):
        print(f"Logging to database: {message}")


class Application:
    def __init__(self, logger: ILogger):
        self.logger = logger  # Depends on abstract ILogger

    def start(self):
        self.logger.log("Application started successfully.")


# ==========================================
# MAIN EXECUTION BLOCK
# ==========================================
if __name__ == '__main__':
    # --- TEST SRP ---
    print("=== TEST SRP (Single Responsibility Principle) ===")
    products = [
        {"name": "Fruit", "price": 50},
        {"name": "Vegetables", "price": 100},
        {"name": "Bread", "price": 20},
        {"name": "Meat", "price": 1000},
    ]

    my_order = Order(products)
    total = my_order.calculate_total()
    print("Total order:", total, "$")
    print("-" * 40)

    printer = OrderPrinter()
    printer.print_order(my_order)
    print("-" * 40)

    repository = OrderRepository()
    repository.save_to_db(my_order)

    print("\n" + "=" * 40 + "\n")

    # --- TEST OCP ---
    print("=== TEST OCP (Open/Closed Principle) ===")
    price = 1000

    regular_discount = Discount(price)
    vip_discount = VIPDiscount(price)
    first_time_discount = FirstTimeDiscount(price)

    print(f"Regular Customer Price: ${regular_discount.apply_discount()}")
    print(f"VIP Customer Price (20% off): ${vip_discount.apply_discount()}")
    print(f"First-Time Customer Price (15% off): ${first_time_discount.apply_discount()}")

    print("\n" + "=" * 40 + "\n")

    # --- TEST LSP ---
    print("=== TEST LSP (Liskov Substitution Principle) ===")
    rect = Rectangle(5, 10)
    sq = Square(5)

    print_area(rect)
    print_area(sq)

    print("-" * 40)
    emp = Employee("Ahmed", "ahmed@univ.dz", 80000)
    std = Student("Amina", "amina@student.univ.dz", "2026123")

    print(f"Employee: {emp.name}, Salary: {emp.get_salary()} DZD")
    emp.assign_task("Grade lab work")
    print(f"Student: {std.name}, ID: {std.student_id}")

    print("\n" + "=" * 40 + "\n")

    # --- TEST ISP ---
    print("=== TEST ISP (Interface Segregation Principle) ===")
    print("1. Printers:")
    basic_printer = BasicPrinter()
    basic_printer.print_document("Report.pdf")

    print("-" * 20)
    adv_printer = AdvancedPrinter()
    adv_printer.print_document("Project.pdf")
    adv_printer.scan_document("Image.jpg")
    adv_printer.fax_document("Contract.pdf")

    print("\n2. Academic Roles:")
    prof = ProfessorResearcher()
    print("- Professor Researcher:")
    prof.teach()
    prof.research()

    print("-" * 20)
    researcher = FullTimeResearcher()
    print("- Full-Time Researcher:")
    researcher.research()

    print("-" * 20)
    hospital_prof = ProfessorHospitalResearcher()
    print("- Professor Hospital Researcher:")
    hospital_prof.teach()
    hospital_prof.research()
    hospital_prof.practice_medicine()

    print("\n" + "=" * 40 + "\n")

    # --- TEST DIP ---
    print("=== TEST DIP (Dependency Inversion Principle) ===")
    print("1. Notification Services:")
    email_notifier = Notification(EmailService())
    email_notifier.send("Hello via Email!")

    sms_notifier = Notification(SMSService())
    sms_notifier.send("Hello via SMS!")

    push_notifier = Notification(PushNotificationService())
    push_notifier.send("Hello via Push Notification!")

    print("\n2. Application Logging (Application / Logger):")
    file_logger = FileLogger()
    app_with_file = Application(file_logger)
    app_with_file.start()

    db_logger = DatabaseLogger()
    app_with_db = Application(db_logger)
    app_with_db.start()