import sys

def read_float(msg):
    while True:
        raw = input(msg).strip().replace(',', '.')
        try:
            return float(raw)
        except ValueError:
            print("Некорректное число, попробуйте снова.")

def read_interval():
    while True:
        x0 = read_float("Введите x0: ")
        xn = read_float("Введите xn (xn > x0): ")
        if xn <= x0:
            print("xn должно быть больше x0. Попробуйте снова.")
        else:
            return x0, xn

def read_pos(msg):
    while True:
        val = read_float(msg)
        if val <= 0:
            print("Значение должно быть > 0. Попробуйте снова.")
        else:
            return val

def read_eps():
    return read_pos("Введите точность eps (>0): ")

def read_step(x0, xn):
    while True:
        h = read_pos("Введите шаг h (>0): ")
        n_f = (xn - x0) / h
        if abs(round(n_f) - n_f) > 1e-8:
            print("Шаг h не делит интервал [x0,xn] на равные части. Попробуйте снова.")
        else:
            return h, int(round(n_f))
