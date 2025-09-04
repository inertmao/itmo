import sympy as sp
from scipy.optimize import minimize_scalar
import numpy as np
from exceptions import *
from utils import *

def chord_method(f, a, b, eps):
    n = 0
    x = a - f(a) * (b - a) / (f(b) - f(a))

    while abs(f(x)) >= eps:
        if f(a) * f(x) < 0:
            b = x
        else:
            a = x
        x = a - f(a) * (b - a) / (f(b) - f(a))
        n += 1

    return x, f(x), n

def newton_single(g, a, b, eps):
    
    n = 0
    x = sp.symbols('x')
    
    f = g(x)
    
    df = sp.diff(f, x)
    d2f = sp.diff(f, x, 2)
    
    if f.subs(x, a).evalf() * d2f.subs(x, a).evalf() > 0:
        x_i = a
    elif f.subs(x, b).evalf() * d2f.subs(x, b).evalf() > 0:
        x_i = b
    else:
        x_i = (a + b) / 2
    
    while True:
        n += 1
        x_prev = x_i
        x_i = x_prev - f.subs(x, x_prev).evalf() / df.subs(x, x_prev).evalf()
        
        if abs(x_i - x_prev) <= eps or abs(f.subs(x, x_i).evalf() / df.subs(x, x_prev).evalf()) <= eps or abs(f.subs(x, x_i).evalf()) <= eps:
            break
        
    return x_i, f.subs(x, x_i).evalf(), n
    
    
def simple_iteration(g, a, b, eps):
    n = 0
    x = sp.symbols('x')
    
    f = g(x)
    
    if not (is_increasing(f, a, b) or is_decreasing(f, a, b)):
        raise NotMonotonic("Функция не монотонна на заданном отрезке")
        
    
    df = sp.diff(f, x)
    d2f = sp.diff(f, x, 2)    
        
    if f.subs(x, a).evalf() * d2f.subs(x, a).evalf() > 0:
        x_i = a
    elif f.subs(x, b).evalf() * d2f.subs(x, b).evalf() > 0:
        x_i = b
    else:
        x_i = (a + b) / 2
        
        
    mx = max(abs( df.subs(x, a).evalf() ), abs( df.subs(x, b).evalf() ))
    lmbd = 1 / mx
        
    if is_increasing(df, a, b):
        pass
        
    elif is_decreasing(df, a, b): 
        lmbd = -lmbd

    phi = x + lmbd * f
    
    
    dphi = sp.diff(phi, x)
    for point in np.linspace(a, b, 100):
        value = abs( dphi.subs(x, point).evalf() )
        if value > 1:
            raise NotCoverage("Метод не сходится на заданном отрезке")
    
    while True:
        n += 1
        prev = x_i
        x_i = phi.subs(x, prev).evalf()
        if abs(x_i - prev) <= eps:
            break
    return prev, g(prev), n

