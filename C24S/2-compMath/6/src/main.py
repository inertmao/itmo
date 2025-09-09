import sys
from problems import problems
from methods import euler, rk4, adams
from utils import read_interval, read_step, read_eps, read_float
from table_printer import print_table
from plotting import plot_all_solutions

def choose_prob():
    print("Выберите ОДУ:")
    print("1: y' = y, y(0)=1, точное: exp(x)")
    print("2: y' = 2*x, y(0)=1, точное: x^2 + 1")
    print("3: y' = y - x^2 + 1, y(0)=0.5, точное: (x+1)^2 - 0.5*exp(x)")
    while True:
        try:
            ch = int(input("Ваш выбор (1-3): "))
            if ch in problems:
                return ch
            else:
                print("Введите число от 1 до 3.")
        except ValueError:
            print("Некорректный ввод.")

def main_run():
    print("--- Решение ОДУ ---")
    ch = choose_prob()
    f, exact, x0_def, y0_def = problems[ch]
    print(f"Выбрано ОДУ {ch}")

    # интервал
    x0, xn = read_interval()

    # начальное y
    if x0 != x0_def:
        y0 = read_float(f"Введите y({x0}): ")
    else:
        y0 = y0_def

    # шаг и n
    h, n = read_step(x0, xn)

    # точность
    eps = read_eps()

    # точное решение
    xs = [x0 + i*h for i in range(n+1)]
    y_true = [exact(x) for x in xs]

    # Эйлер и РК4
    xs_e, ys_e = euler(f, x0, y0, h, n)
    xs_r, ys_r = rk4(f, x0, y0, h, n)

    # для Рунге
    h2 = h/2
    n2 = 2*n
    _, ys_e2 = euler(f, x0, y0, h2, n2)
    _, ys_r2 = rk4(f, x0, y0, h2, n2)

    err_e = abs(ys_e2[-1] - ys_e[-1]) / (2**1 - 1)
    err_r = abs(ys_r2[-1] - ys_r[-1]) / (2**4 - 1)

    print(f"Ошибка Эйлера (Runge): {err_e:.6e}")
    print(f"Ошибка РК4 (Runge): {err_r:.6e}")

    # Адамс
    xs_a, ys_a, err_a = adams(f, x0, y0, h, n, exact)
    print(f"Макс. ошибка Адамса (сравнение с точным): {err_a:.6e}")

    # таблица
    print_table(xs, ys_e, ys_r, ys_a, y_true)

    # график
    plot_all_solutions(xs, y_true, ys_e, ys_r, ys_a)

if __name__ == "__main__":
    while True:
        try:
            main_run()
            cont = input("Ещё раз? (y/n): ").strip().lower()
            if cont != 'y':
                print("Выход.")
                break
        except Exception as e:
            print(f"Ошибка: {e}")
            print("Попробуйте снова.")
