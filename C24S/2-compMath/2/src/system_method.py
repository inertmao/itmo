import numpy as np
from utils import *


def F1(z):

    x, y = z[0], z[1]
    return np.array([
        x**2 + y**2 - 25,
        x**2 - y - 5
    ])

def J1(z):

    x, y = z[0], z[1]
    return np.array([
        [2*x,     2*y],
        [2*x, -1]
    ])


def F2(z):

    x, y = z[0], z[1]
    return np.array([
        np.exp(x) + y - 4,
        x + np.sin(y) - 1
    ])

def J2(z):

    x, y = z[0], z[1]
    return np.array([
        [np.exp(x), y],
        [1, np.cos(y)]
    ])
    
def newton_system(F, J, z0, eps):
    n = 0
    error_history = []
    z = z0.copy()
    while True:
        n += 1
        Fz = F(z)
        Jz = J(z)
        delta = np.linalg.solve(Jz, Fz)
        z_new = z - delta
        error_vector = np.abs(z_new - z)
        error_history.append(error_vector.copy())   
        if np.all(np.abs(z_new - z) <= eps) and np.all(np.abs(F(z_new) - F(z)) <= eps):
            return z_new, n, error_history
        
        z = z_new

