# src/utils/calculator.py

import math

class Calculator:
    @staticmethod
    def calculate_function(x: float, eq: int) -> float:
        if eq == 1:
            return 2*x**3 + 3.41*x**2 - 23.74*x + 2.95
        elif eq == 2:
            val = 23.9 * x + 6
            if val < 0:
                raise ValueError(f"Недопустимый аргумент для sqrt: 23.9*{x:.3f}+6 = {val:.3f} < 0")
            return math.sqrt(val) - 239
        elif eq == 3:
            return math.cos(x) + 0.5
        else:
            return 0.0

    @staticmethod
    def calculate_derivative(x: float, eq: int) -> float:
        if eq == 1:
            return 6*x**2 + 6.82*x - 23.74
        elif eq == 2:
            val = 23.9 * x + 6
            if val <= 0:
                raise ValueError(f"Недопустимый аргумент для sqrt в производной: 23.9*{x:.3f}+6 = {val:.3f} ≤ 0")
            return 11.95 / math.sqrt(val)
        elif eq == 3:
            return -math.sin(x)
        else:
            return 0.0

    @staticmethod
    def calculate_second_derivative(x: float, eq: int) -> float:
        if eq == 1:
            return 12*x + 6.82
        elif eq == 2:
            # для второй производной аргумент под корнем тот же
            val = 23.9 * x + 6
            if val <= 0:
                raise ValueError(f"Недопустимый аргумент для sqrt во второй производной: 23.9*{x:.3f}+6 = {val:.3f} ≤ 0")
            return -142.802 / (val**1.5)
        elif eq == 3:
            return -math.cos(x)
        else:
            return 0.0

    @staticmethod
    def calculate_phi(x: float, eq: int, λ: float) -> float:
        return Calculator.calculate_function(x, eq) * λ + x

    @staticmethod
    def calculate_phi_derivative(x: float, eq: int, λ: float) -> float:
        if eq == 1:
            return 6*λ*(x**2 + 1.13667*x - 3.95667) + 1
        elif eq == 2:
            val = 23.9 * x + 6
            if val <= 0:
                raise ValueError(f"Недопустимый аргумент для sqrt в φ' для eq=2: {val:.3f} ≤ 0")
            return 11.95 * λ / math.sqrt(val) + 1
        elif eq == 3:
            return 1 - λ * math.sin(x)
        else:
            return 0.0
