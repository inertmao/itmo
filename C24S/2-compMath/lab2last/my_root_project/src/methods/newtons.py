import math
from utils.calculator import Calculator
from utils.colorful_string import ColorfulString
from utils.graph import Graph
from methods.half_division import HalfDivision
class Newtons:
    @staticmethod
    def verify_existing(a, b, eq):
        return HalfDivision.verify_existing(a, b, eq)

    @staticmethod
    def verify_singularity(a, b, eq):
        return HalfDivision.verify_singularity(a, b, eq)

    @staticmethod
    def verify_second_derivative(a, b, eq):
        step = (b - a) / 100
        x, sign = a, math.copysign(1, Calculator.calculate_second_derivative(a, eq))
        while x < b:
            x += step
            if math.copysign(1, Calculator.calculate_second_derivative(x, eq)) != sign:
                return False
        return True

    @staticmethod
    def choose_initial(a, b, eq):
        if Calculator.calculate_function(a,eq)*Calculator.calculate_second_derivative(a,eq) > 0:
            return a
        else:
            return b

    @staticmethod
    def decimal_places(ε):
        return HalfDivision.decimal_places(ε)

    @staticmethod
    def print_iter(i, ε, xk, f, df, xk1):
        d = Newtons.decimal_places(ε)
        print(f"{i}) xk={xk:.{d}f}, f(xk)={f:.{d}f}, f'(xk)={df:.{d}f}, xk+1={xk1:.{d}f}, |xk-xk+1|={abs(xk-xk1):.{d}f}")

    @staticmethod
    def print_result(x0, eq, ε, count):
        d = Newtons.decimal_places(ε)
        print("Результат:")
        print(f"Найденный корень уравнения: {x0:.{d}f}")
        print(f"Значение функции в корне: {Calculator.calculate_function(x0,eq):.{d}f}")
        print(f"Число итераций: {count}")

    @staticmethod
    def solve(a, b, ε, eq):
        Graph(a, b, eq)
        while not Newtons.verify_existing(a,b,eq):
            ColorfulString.println("Введите левую границу интервала.")
            a = float(input())
            ColorfulString.println("Введите правую границу интервала.")
            b = float(input())
        if not Newtons.verify_singularity(a,b,eq):
            ColorfulString.println("На данном промежутке корень может быть не единственный.")
        while not Newtons.verify_second_derivative(a,b,eq):
            ColorfulString.println("Не пройдена проверка второй производной.")
            a = float(input()); b = float(input())
        i = 1
        xk = Newtons.choose_initial(a,b,eq)
        f = Calculator.calculate_function(xk, eq)
        df = Calculator.calculate_derivative(xk, eq)
        xk1 = xk - f/df
        Newtons.print_iter(i, ε, xk, f, df, xk1)
        while not (abs(xk1-xk) <= ε or abs(f/df) <= ε or abs(f) <= ε):
            xk = xk1
            f  = Calculator.calculate_function(xk, eq)
            df = Calculator.calculate_derivative(xk, eq)
            xk1 = xk - f/df
            i += 1
            Newtons.print_iter(i, ε, xk, f, df, xk1)
        Newtons.print_result(xk1, eq, ε, i)
