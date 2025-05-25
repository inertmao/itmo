import math
from utils.calculator import Calculator
from utils.colorful_string import ColorfulString
from utils.graph import Graph

class HalfDivision:
    @staticmethod
    def verify_existing(a: float, b: float, eq: int) -> bool:
        if Calculator.calculate_function(a, eq) * Calculator.calculate_function(b, eq) < 0:
            return True
        ColorfulString.println("Не пройдена верификация существования и единственности корня на данном промежутке.")
        return False

    @staticmethod
    def verify_singularity(a: float, b: float, eq: int) -> bool:
        step = (b - a) / 100
        x, sign = a, math.copysign(1, Calculator.calculate_derivative(a, eq))
        while x < b:
            x += step
            if math.copysign(1, Calculator.calculate_derivative(x, eq)) != sign:
                return False
        return True

    @staticmethod
    def decimal_places(ε: float) -> int:
        cnt, q = 1, 0.1
        while q >= ε:
            q /= 10
            cnt += 1
        return cnt

    @staticmethod
    def print_iter(a, b, x0, f, eq, ε, i):
        d = HalfDivision.decimal_places(ε)
        print(f"{i}) a={a:.{d}f}, b={b:.{d}f}, x={x0:.{d}f}, "
              f"f(a)={Calculator.calculate_function(a,eq):.{d}f}, "
              f"f(b)={Calculator.calculate_function(b,eq):.{d}f}, "
              f"f(x)={f:.{d}f}, |a-b|={abs(b-a):.{d}f}")

    @staticmethod
    def print_result(x0, eq, ε, count):
        d = HalfDivision.decimal_places(ε)
        print("Результат:")
        print(f"Найденный корень уравнения: {x0:.{d}f}")
        print(f"Значение функции в корне: {Calculator.calculate_function(x0, eq):.{d}f}")
        print(f"Число итераций: {count}")

    @staticmethod
    def solve(a: float, b: float, ε: float, eq: int):
        Graph(a, b, eq)
        while not HalfDivision.verify_existing(a, b, eq):
            ColorfulString.println("Введите левую границу интервала.")
            a = float(input())
            ColorfulString.println("Введите правую границу интервала.")
            b = float(input())
        if not HalfDivision.verify_singularity(a, b, eq):
            ColorfulString.println("На данном промежутке корень может быть не единственный.")
        ColorfulString.println("Выводить процесс решения в файл? [y]/[n]")
        if input().lower() == 'y':
            with open("result.txt", "w") as f:
                i, x0 = 1, (a+b)/2
                f0 = Calculator.calculate_function(x0, eq)
                f.write(f"{i}) a={a}, b={b}, x={x0}, f(a)={Calculator.calculate_function(a,eq)}, "
                        f"f(b)={Calculator.calculate_function(b,eq)}, f(x)={f0}, |a-b|={abs(b-a)}\n")
                while not (abs(b-a) <= ε or abs(f0) <= ε):
                    if Calculator.calculate_function(a,eq)*f0 < 0:
                        b = x0
                    else:
                        a = x0
                    x0 = (a+b)/2
                    f0 = Calculator.calculate_function(x0, eq)
                    i += 1
                    f.write(f"{i}) a={a}, b={b}, x={x0}, f(a)={Calculator.calculate_function(a,eq)}, "
                            f"f(b)={Calculator.calculate_function(b,eq)}, f(x)={f0}, |a-b|={abs(b-a)}\n")
                HalfDivision.print_result(x0, eq, ε, i)
            return
        # вывод в консоль
        i, x0 = 1, (a+b)/2
        f0 = Calculator.calculate_function(x0, eq)
        HalfDivision.print_iter(a, b, x0, f0, eq, ε, i)
        while not (abs(b-a) <= ε or abs(f0) <= ε):
            if Calculator.calculate_function(a,eq)*f0 < 0:
                b = x0
            else:
                a = x0
            x0 = (a+b)/2
            f0 = Calculator.calculate_function(x0, eq)
            i += 1
            HalfDivision.print_iter(a, b, x0, f0, eq, ε, i)
        HalfDivision.print_result(x0, eq, ε, i)

