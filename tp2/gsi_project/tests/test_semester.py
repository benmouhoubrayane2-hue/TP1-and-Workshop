from module import Module
from unit import Unit
from semester import Semester

def test_semester_calculations():
    m1 = Module("M111", "Database", coef=2, credit=4, hours_tp=1.5)
    m1.set_grade(tp=14, exam=14)
    
    u1 = Unit("UEM11", "UE Methodologie", [m1])
    sem = Semester("S1", "Semestre 1", [u1])
    
    assert sem.calculate_average() >= 10
    assert sem.calculate_credits() == 4