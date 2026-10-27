from module import Module

def test_module_initialization():
    m = Module(name="MTI", title="Methods and Technologies", coef=3, credit=5)
    assert m.name == "MTI"
    assert m.coef == 3
    assert m.credit == 5

def test_module_grades_and_average():
    m = Module(name="MTI", title="Methods and Technologies", coef=3, credit=5, hours_tp=1.5, continous_percent=40, exam_percent=60)
    m.set_grade(tp=14, exam=14)
    avg = m.calculate_average()
    assert avg >= 10
    
def test_module_credits():
    m = Module(name="MTI", title="Methods and Technologies", coef=3, credit=5, hours_tp=1.5)
    m.set_grade(tp=14, exam=14)  # Assure une moyenne >= 10 pour valider les crédits
    assert m.calculate_credits() == 5
    
    # Une mauvaise note doit retourner 0 crédits
    m.set_grade(tp=2, exam=4)
    assert m.calculate_credits() == 0