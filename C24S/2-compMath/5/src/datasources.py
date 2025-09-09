import math
import csv

def read_keyboard():
    x, y = [], []
    print("Введите точки (x y). Пустая строка = конец:")
    while True:
        try:
            line = input().strip()
            if not line:
                break
            parts = line.replace(',', '.').split()
            if len(parts) != 2:
                print("Нужно два числа: x и y")
                continue
            x_new = float(parts[0])
            y_new = float(parts[1])
            if x_new in x:
                print(f"x={x_new} уже есть, нельзя повторять.")
                continue
            x.append(x_new)
            y.append(y_new)
        except KeyboardInterrupt:
            raise
        except:
            print("Ошибка ввода.")
    return x, y

def read_file():
    fname = input("Имя файла: ")
    x, y = [], []
    try:
        with open(fname, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) < 2:
                    continue
                try:
                    x_new = float(row[0].replace(',', '.'))
                    y_new = float(row[1].replace(',', '.'))
                except:
                    print("Пропуск строки:", row)
                    continue
                if x_new in x:
                    print(f"Пропуск повтора x={x_new}")
                    continue
                x.append(x_new)
                y.append(y_new)
    except Exception as e:
        print("Ошибка файла:", e)
    return x, y

def read_func():
    funcs = {'1': ('sin(x)', math.sin), '2': ('cos(x)', math.cos)}
    while True:
        print("Выберите функцию:")
        for k,(name,_) in funcs.items():
            print(f"{k}: {name}")
        c = input("Ваш выбор: ").strip()
        if c not in funcs:
            print("Неверно.")
            continue
        _, f = funcs[c]
        try:
            a = float(input("Левая граница: ").replace(',', '.'))
            b = float(input("Правая граница: ").replace(',', '.'))
            n = int(input("Число точек (>=2): "))
            if n < 2 or a >= b:
                print("Ошибка интервала.")
                continue
        except KeyboardInterrupt:
            raise
        except:
            print("Ошибка ввода.")
            continue
        xs, ys = [], []
        for i in range(n):
            xi = a + i*(b-a)/(n-1)
            xs.append(xi)
            ys.append(f(xi))
        return xs, ys
