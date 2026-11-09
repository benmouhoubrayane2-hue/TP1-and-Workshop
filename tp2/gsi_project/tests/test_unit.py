from module import Module
from unit import Unit

def test_unit_initialization():
    m1 = Module("M111", "Database", coef=2, credit=4)
    u = Unit("UEM11", "UE Methodologie", [m1])
    assert u.name == "UEM11"
    assert len(u._modules) == 1

def test_unit_calculations():
    m1 = Module("M111", "Database", coef=2, credit=4, hours_tp=1.5, continous_percent=40, exam_percent=60)
    m1.set_grade(tp=14, exam=14)
    
    u = Unit("UEM11", "UE Methodologie", [m1])
    assert u.calculate_average() >= 10
    assert u.calculate_credits() == 4