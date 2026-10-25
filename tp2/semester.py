from academicelement import AcademicElement

class Semester(AcademicElement):
    """Represents a semester containing multiple teaching units (UE)."""
    
    def __init__(self, name, title, units=None):
        super().__init__(name, title)
        self._units = units if units is not None else []

    def add_unit(self, unit):
        """Add a teaching unit to the semester."""
        self._units.append(unit)

    def calculate_average(self):
        """Calculate the overall semester average based on units and module coefficients."""
        if not self._units:
            return 0
        
        total_weighted_grades = 0
        total_coefficients = 0
        
        for unit in self._units:
            for module in unit._modules:
                total_weighted_grades += module.calculate_average() * module.coef
                total_coefficients += module.coef
                
        if total_coefficients == 0:
            return 0
            
        return total_weighted_grades / total_coefficients

    def calculate_credits(self):
        """Calculate total credits earned for the semester."""
        if not self._units:
            return 0
        return sum(unit.calculate_credits() for unit in self._units)

# Example usage and testing
if __name__ == "__main__":
    from module import Module
    from unit import Unit
    
    # 1. Create Modules for Semester 1
    m1 = Module(name="F111", title="Réseaux des couches basses", coef=3, credit=6, hours_tp=1.5)
    m1.set_grade(tp=14, exam=12)
    
    m2 = Module(name="F112", title="Algorithmique Avancée", coef=2, credit=4, hours_tp=1.5)
    m2.set_grade(tp=15, exam=13)
    
    # 2. Create Teaching Unit (UE)
    ue11 = Unit("UEF11", "UE Fondamentale 1", [m1, m2])
    
    # 3. Create Semester
    s1 = Semester("S1", "Semestre 1", [ue11])
    
    print(f"Semester Average: {s1.calculate_average():.2f}")
    print(f"Semester Credits Earned: {s1.calculate_credits()}")