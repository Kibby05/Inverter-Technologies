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

'''

https://www.youtube.com/watch?v=8-V5T40aMEc

Avoided the loop by passing u as a function representing the step function:
def first_order(y, t, tau, K, u):
    dydt = (-y + K*u(t)) / tau
    return dydt


t0 = 0
t1 = 10
intervals = 100
t = np.linspace(t0, t1, intervals)
tau = 5.0
K = 2.0
u = lambda t: 0 if t < 3 else 1
y = odeint(first_order, 0, t, args=(tau, K, u))
plt.plot(t, y)
'''