import sys
import math

# Подключаем утилиты
from utils.colorful_string import ColorfulString
from utils.calculator import Calculator
from utils.graph       import Graph

# Подключаем методы решения
from methods.half_division   import HalfDivision
from methods.newtons         import Newtons
from methods.simple_iteration import SimpleIteration
def read_from_file():
    fname = input(ColorfulString.ANSI_CYAN + "Введите название файла: " + ColorfulString.ANSI_RESET)
    try:
        with open(fname) as f:
            a = float(f.readline())
            b = float(f.readline())
            ε = float(f.readline())
        return a, b, ε
    except FileNotFoundError:
        ColorfulString.println("Файл не найден!")
        sys.exit(1)


def read_from_console():
    ColorfulString.println("Введите левую границу интервала.")
    a = float(input())
    ColorfulString.println("Введите правую границу интервала.")
    b = float(input())
    while b - a <= 0:
        ColorfulString.println("Границы введены неверно, попробуйте ещё раз.")
        a = float(input("Левая граница: "))
        b = float(input("Правая граница: "))
    ColorfulString.println("Введите погрешность вычисления.")
    ε = float(input())
    return a, b, ε


def main():
    equations = ["2*x^3+3.41*x^2-23.74*x+2.95",
                 "(23.9*x+6)^(1/2)-239",
                 "cos(x)+1/2"]
    methods = ["Метод половинного деления", "Метод Ньютона", "Метод простой итерации"]

    ColorfulString.println("Выберите уравнение.")
    for i, eq in enumerate(equations, 1):
        print(f"{i}) {eq}")
    eqn = int(input())
    while eqn not in (1,2,3):
        ColorfulString.println("Попробуйте выбрать номер уравнения ещё раз.")
        eqn = int(input())

    ColorfulString.println("Выберите метод решения уравнения.")
    for i, m in enumerate(methods, 1):
        print(f"{i}) {m}")
    mtd = int(input())
    while mtd not in (1,2,3):
        ColorfulString.println("Попробуйте выбрать метод ещё раз.")
        mtd = int(input())

    ColorfulString.println("Читать исходные данные из файла? [y]/[n]")
    if input().lower() == 'y':
        a,b,ε = read_from_file()
    else:
        a,b,ε = read_from_console()

    if mtd == 1:
        HalfDivision.solve(a, b, ε, eqn)
    elif mtd == 2:
        Newtons.solve(a, b, ε, eqn)
    else:
        SimpleIteration.solve(a, b, ε, eqn)


if __name__ == "__main__":
    main()
