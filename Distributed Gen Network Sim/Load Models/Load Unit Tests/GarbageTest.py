class Salary:
    def __init__(self, pay, bonus, poop):
        self.pay = pay
        self.bonus = bonus
        self.poop = poop
    
    def annual_salary(self):
        return (self.pay*12) + self.bonus

class Employee(object):
    def __init__(self, name, age, salary, *args):
        super(Employee, self).__init__(*args)
        self.name=name
        self.age=age
        self.obj_salary=salary
    def total_salary(self):
        return self.obj_salary.annual_salary()

Salary = Salary(1500, 100000, 3)

emp = Employee("pooopppooo", 25, Salary)
print(emp.total_salary())
        