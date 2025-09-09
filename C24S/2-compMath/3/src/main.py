import math
import numpy as np

# ===== Методы =====
def left_rect(f, a, b, n):
    h = (b - a) / n
    s = 0
    for i in range(n):
        s += f(a)
        a += h
    return h * s

def right_rect(f, a, b, n):
    h = (b - a) / n
    s = 0
    for i in range(n):
        a += h
        s += f(a)
    return h * s

def mid_rect(f, a, b, n):
    h = (b - a) / n
    s = 0
    a += h / 2
    for i in range(n):
        s += f(a)
        a += h
    return h * s

def trapezoid(f, a, b, n):
    h = (b - a) / n
    s = 0
    y0 = f(a)
    yn = f(b)
    for i in range(1, n):
        a += h
        s += f(a)
    return h * ((y0 + yn) / 2 + s)

def simpson(f, a, b, n):
    h = (b - a) / n
    s = 0
    y0 = f(a)
    yn = f(b)
    for i in range(1, n):
        a += h
        if i % 2 == 0:
            s += 2 * f(a)
        else:
            s += 4 * f(a)
    return h / 3 * (y0 + s + yn)

# ===== Правило Рунге =====
def runge(method, f, a, b, n, eps, k):
    i1 = method(f, a, b, n)
    i2 = method(f, a, b, 2*n)
    err = (i2 - i1) / (2**k - 1)

    while abs(err) >= eps:
        n *= 2
        i1 = i2
        i2 = method(f, a, b, 2*n)
        err = (i2 - i1) / (2**k - 1)

    return 2*n

# ===== Ввод =====
def parse_num(x):
    try:
        return float(x.replace(',', '.'))
    except:
        raise ValueError("Ошибка ввода: " + x)

def get_data(msgs):
    vals = []
    for m in msgs:
        vals.append(parse_num(input(m)))
    return vals

# ===== Основная программа =====
def main():
    N = 4
    methods = {
        "1": {"1": (left_rect, 1), "2": (right_rect, 1), "3": (mid_rect, 2)},
        "2": (trapezoid, 2),
        "3": (simpson, 4)
    }

    while True:
        # выбор функции
        while True:
            print("Выберите функцию:")
            print("1 - x^3 + 2x^2 - 5x + 1")
            print("2 - exp(2x)*log(x)")
            print("3 - sin(x)^3 * cos(x)^2")
            print("4 - 2x^20 - 3x^15 + x^10 - 5x^5 + 7")
            f_choice = input("Введите номер: ").strip()

            if f_choice == "1":
                f = lambda x: x**3 + 2*x**2 - 5*x + 1
                break
            elif f_choice == "2":
                f = lambda x: math.e**(2*x) * math.log(x)
                break
            elif f_choice == "3":
                f = lambda x: np.sin(x)**3 * np.cos(x)**2
                break
            elif f_choice == "4":
                f = lambda x: 2*x**20 - 3*x**15 + x**10 - 5*x**5 + 7
                break
            else:
                print("Неверный выбор")

        # выбор метода
        while True:
            print("Выберите метод:")
            print("1 - Прямоугольники")
            print("2 - Трапеции")
            print("3 - Симпсон")
            m_choice = input("Введите номер: ").strip()

            if m_choice == "1":
                print("1 - левые\n2 - правые\n3 - средние")
                mod = input("Введите номер: ").strip()
                if mod in ["1", "2", "3"]:
                    method, k = methods[m_choice][mod]
                    break
                else:
                    print("Неверная модификация")
            elif m_choice in ["2", "3"]:
                method, k = methods[m_choice]
                break
            else:
                print("Неверный выбор")

        # ввод данных
        while True:
            try:
                a, b, eps = get_data(["Левый предел: ", "Правый предел: ", "Точность: "])
                break
            except Exception as e:
                print(e)

        n = runge(method, f, a, b, N, eps, k)
        ans = method(f, a, b, n)

        print(f"\nИнтеграл = {ans}")
        print(f"Разбиение n = {n} для точности {eps}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nВыход...")
