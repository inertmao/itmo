import math

def problems_menu():
    return {
        1: ("y' = y", "y(0) = 1", f1, y_exp),
        2: ("y' = 2*x", "y(0) = 1", f2, y_quad),
        3: ("y' = y - x^2 + 1", "y(0) = 0.5", f3, y_cust)
    }

# ===== Задачи =====
# 1: y' = y, y(0)=1, exact y = e^x
def f1(x, y): return y
def y_exp(x): return math.exp(x)

# 2: y' = 2*x, y(0)=1, exact y = x^2 + 1
def f2(x, y): return 2*x
def y_quad(x): return x**2 + 1

# 3: y' = y - x^2 + 1, y(0)=0.5, exact y = (x+1)^2 - 0.5*e^x
def f3(x, y): return y - x**2 + 1
def y_cust(x): return (x+1)**2 - 0.5*math.exp(x)

# ===== Для main =====
problems = {
    1: (f1, y_exp, 0.0, 1.0),   # (f, exact, x0, y0)
    2: (f2, y_quad, 0.0, 1.0),
    3: (f3, y_cust, 0.0, 0.5)
}
