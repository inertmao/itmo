import sympy as sp
from scipy.optimize import minimize_scalar
import numpy as np
from exceptions import *


def get_max_f(f, a, b):
    result = minimize_scalar(lambda z: -f(z), bounds=(a, b), method='bounded')
    return result.x

def get_min_f(f, a, b):
    result = minimize_scalar(f, bounds=(a, b), method='bounded')
    return result.x

def get_max_abs_f(f, a, b):
    return max(abs(f(a)), abs(f(b)))
    
def is_increasing(f, a, b):
    is_increasing = True

    x = sp.symbols('x')
    df = sp.diff(f, x)
    
    for point in np.linspace(a, b, 100):
        value = df.subs(x, point).evalf()
        if value < 0:
            is_increasing = False
    
    return is_increasing

def is_decreasing(f, a, b):
    is_decreasing = True
    
    x = sp.symbols('x')
    df = sp.diff(f, x)
    
    for point in np.linspace(a, b, 100):
        value = df.subs(x, point).evalf()
        if value > 0:
            is_decreasing = False

    return is_decreasing

def count_sign_changes(f, a, b, num_points=2000):
    x_vals = np.linspace(a, b, num_points)
    f_vals = np.array([f(x) for x in x_vals])
    sign_changes = np.sum(np.diff(np.sign(f_vals)) != 0)
    return sign_changes
