import math
from utils.calculator import Calculator
from utils.colorful_string import ColorfulString
from utils.graph import Graph
from methods.half_division import HalfDivision 
class SimpleIteration:
    λ = None

    @staticmethod
    def verify_existing(a,b,eq):
        return HalfDivision.verify_existing(a,b,eq)

    @staticmethod
    def verify_singularity(a,b,eq):
        return HalfDivision.verify_singularity(a,b,eq)

    @staticmethod
    def verify_convergence(a,b,eq):
        step = (b - a)/50
        SimpleIteration.λ = -1 / max(
            Calculator.calculate_derivative(a,eq),
            Calculator.calculate_derivative(b,eq)
        )
        x = a
        while x < b:
            x += step
            if abs(Calculator.calculate_phi_derivative(x,eq,SimpleIteration.λ)) >= 1:
                return False
        return True

    @staticmethod
    def decimal_places(ε):
        return HalfDivision.decimal_places(ε)

    @staticmethod
    def print_iter(i, ε, xk, f, xk1):
        d = SimpleIteration.decimal_places(ε)
        print(f"{i}) xk={xk:.{d}f}, f(xk)={f:.{d}f}, xk+1={xk1:.{d}f}, |xk-xk+1|={abs(xk1-xk):.{d}f}")

    @staticmethod
    def print_result(x0, eq, ε, cnt):
        d = SimpleIteration.decimal_places(ε)
        print("Результат:")
        print(f"Найденный корень уравнения: {x0:.{d}f}")
        print(f"Значение функции в корне: {Calculator.calculate_function(x0,eq):.{d}f}")
        print(f"Число итераций: {cnt}")

    @staticmethod
    def solve(a,b,ε,eq):
        Graph(a,b,eq)
        while not SimpleIteration.verify_existing(a,b,eq):
            ColorfulString.println("Введите левую границу интервала.")
            a = float(input())
            ColorfulString.println("Введите правую границу интервала.")
            b = float(input())
        if not SimpleIteration.verify_singularity(a,b,eq):
            ColorfulString.println("На данном промежутке корень может быть не единственный.")
        while not SimpleIteration.verify_convergence(a,b,eq):
            ColorfulString.println("Условие сходимости не выполнено.")
            a = float(input()); b = float(input())
        i, xk = 1, a
        f = Calculator.calculate_function(xk,eq)
        xk1 = Calculator.calculate_phi(xk,eq,SimpleIteration.λ)
        SimpleIteration.print_iter(i, ε, xk, f, xk1)
        while True:
            q = abs(Calculator.calculate_phi_derivative(xk1,eq,SimpleIteration.λ))
            if (q <= 0.5 and abs(xk1-xk) <= ε) or (q > 0.5 and abs(xk1-xk) <= (1-q)*ε/q):
                break
            xk, xk1 = xk1, Calculator.calculate_phi(xk1,eq,SimpleIteration.λ)
            f = Calculator.calculate_function(xk,eq)
            i += 1
            SimpleIteration.print_iter(i, ε, xk, f, xk1)
        SimpleIteration.print_result(xk1, eq, ε, i)
