from academicelement import AcademicElement

class Unit(AcademicElement):
    """Represents a teaching unit containing multiple modules."""
    
    def __init__(self, name, title, modules=None):
        super().__init__(name, title)
        self._modules = modules if modules is not None else []

    def add_module(self, module):
        """Add a module to the unit."""
        self._modules.append(module)

    def calculate_average(self):
        """Example of aggregation combining module averages."""
        if not self._modules:
            return 0
        total = sum(m.calculate_average() * m.coef for m in self._modules)
        coef_sum = sum(m.coef for m in self._modules)
        if coef_sum == 0:
            return 0
        return total / coef_sum

    def calculate_credits(self):
        """Polymorphism: different modules could override this behavior."""
        if not self._modules:
            return 0
        avg = self.calculate_average()
        if avg >= 10:
            return sum(m.credit for m in self._modules)
        else:
            return sum(m.calculate_credits() for m in self._modules)