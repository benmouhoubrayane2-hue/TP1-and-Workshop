from academicelement import AcademicElement

class Module(AcademicElement):
    """
    Represents a teaching module with pedagogical and evaluation attributes.
    """
    def __init__(
        self,
        name: str = "", # Module code
        title: str = "",
        coef: int = 1,
        credit: int = 1,
        hours_lecture: float = 1.5,
        hours_td: float = 0,
        hours_tp: float = 0,
        teaching_mode: str = "In-person", # "Distance" or "In-person"
        continous_percent: int = 40,
        exam_percent: int = 60
    ):
        # Call the constructor of the parent class (AcademicElement)[cite: 32]
        super().__init__(name, title)
        
        self.coef = coef
        self.credit = credit

        # Workload distribution (volume horaire)
        self.hours_lecture = hours_lecture
        self.hours_td = hours_td
        self.hours_tp = hours_tp

        # Teaching and evaluation modes
        self.teaching_mode = teaching_mode
        self.evaluation_continous_percent = continous_percent
        self.evaluation_exam_percent = exam_percent

        # Total hours per semester (self._WEEKS is inherited from AcademicElement)
        self.total_hours = self._WEEKS * (self.hours_lecture + self.hours_td + self.hours_tp)
        self._grades = {"tp": 0, "td": 0, "exam": 0}

    # Encapsulation: controlled access to grades
    def set_grade(self, tp=None, td=None, exam=None):
        if tp is not None:
            self._grades["tp"] = tp
        if td is not None:
            self._grades["td"] = td
        if exam is not None:
            self._grades["exam"] = exam

    def summary(self):
        """Return a short textual description of the module."""
        return (
            f"Module: {self.title} ({self.name})\n"
            f"Coefficient: {self.coef}, Credits: {self.credit}\n"
            f"Hours: total {self.total_hours}h ({self.hours_lecture} Lecture, "
            f"{self.hours_td} TD, {self.hours_tp} TP)\n"
            f"Teaching mode: {self.teaching_mode}\n"
            f"Evaluation mode: Continuous: {self.evaluation_continous_percent}% "
            f"Exam: {self.evaluation_exam_percent}%"
        )

    def calculate_average(self):
        """Calculate the module average based on grades and evaluation percentages[cite: 30, 31]."""
        tp = self._grades["tp"] if self._grades["tp"] is not None else 0
        td = self._grades["td"] if self._grades["td"] is not None else 0
        exam = self._grades["exam"] if self._grades["exam"] is not None else 0
        
        percent_exam = self.evaluation_exam_percent
        percent_tp = 0
        percent_td = 0
        
        # Continuous assessment distribution depending on TP and/or TD availability
        if self.hours_tp and self.hours_td:
            percent_tp = self.evaluation_continous_percent / 2
            percent_td = self.evaluation_continous_percent / 2
        elif self.hours_td:
            percent_td = self.evaluation_continous_percent
        elif self.hours_tp:
            percent_tp = self.evaluation_continous_percent
            
        return (
            tp * percent_tp / 100 +
            td * percent_td / 100 +
            exam * percent_exam / 100
        )

    def calculate_credits(self):
        """Return module credits if average is >= 10, otherwise 0[cite: 31]."""
        avg = self.calculate_average()
        if avg >= 10:
            return self.credit
        else:
            return 0

# Example usage and testing
if __name__ == "__main__":
    m1 = Module(
        name="MTI",
        title="Methods & Technologies of Implementation",
        coef=3,
        credit=5,
        hours_tp=1.5,
        continous_percent=40,
        exam_percent=60
    )
    m1.set_grade(tp=10, exam=12)
    
    print(m1.summary())
    print("Module average:", m1.name, m1.calculate_average())
    print("Module credits:", m1.calculate_credits())