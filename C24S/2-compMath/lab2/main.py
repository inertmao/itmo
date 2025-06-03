# main.py

import sys
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt


# ======================= HELPERS =======================

def to_float(s):
    try:
        return float(s.replace(',', '.'))
    except:
        raise ValueError(f"Неверный формат числа: {s}")


def input_three():
    """
    Запрашивает у пользователя три числа: a, b и ε.
    """
    try:
        a = to_float(input("a = "))
        b = to_float(input("b = "))
        eps = to_float(input("ε = "))
        return a, b, eps
    except Exception as e:
        print("Ошибка ввода:", e)
        return None


def load_three(path):
    """
    Читает из файла путь path: три числа (в одну строку через пробел или по строкам).
    """
    try:
        with open(path, encoding='utf-8') as f:
            lines = [ln.strip() for ln in f if ln.strip()]
        if len(lines) == 1:
            parts = lines[0].split()
            return to_float(parts[0]), to_float(parts[1]), to_float(parts[2])
        else:
            return to_float(lines[0]), to_float(lines[1]), to_float(lines[2])
    except Exception as e:
        print("Ошибка чтения:", e)
        return None


def write_text(path, txt):
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(txt)
    except Exception as e:
        print("Ошибка записи:", e)


def count_roots(fun, a, b, pts=2000):
    xs = np.linspace(a, b, pts)
    ys = np.array([fun(x) for x in xs])
    return np.sum(np.diff(np.sign(ys)) != 0)


def der(expr, var):
    return sp.diff(expr, var)


def mono_up(expr, a, b, var):
    d1 = der(expr, var)
    for xv in np.linspace(a, b, 100):
        if float(d1.subs(var, xv)) < 0:
            return False
    return True


def mono_down(expr, a, b, var):
    d1 = der(expr, var)
    for xv in np.linspace(a, b, 100):
        if float(d1.subs(var, xv)) > 0:
            return False
    return True


def secant(fun, x0, x1, tol):
    i = 0
    prev = x0
    cur = x1
    while True:
        i += 1
        fprev = fun(prev)
        fcur = fun(cur)
        if fcur - fprev == 0:
            break
        nxt = cur - fcur * (cur - prev) / (fcur - fprev)
        if abs(fun(nxt)) < tol or abs(nxt - cur) < tol:
            return nxt, fun(nxt), i
        prev, cur = cur, nxt
    return cur, fun(cur), i


def newton_single(expr, var, a, b, tol):
    f = expr
    df = der(f, var)
    d2f = der(df, var)
    if float(f.subs(var, a) * d2f.subs(var, a)) > 0:
        xk = a
    elif float(f.subs(var, b) * d2f.subs(var, b)) > 0:
        xk = b
    else:
        xk = (a + b) / 2
    i = 0
    while True:
        i += 1
        fv = float(f.subs(var, xk))
        dfv = float(df.subs(var, xk))
        if dfv == 0:
            break
        nxt = xk - fv / dfv
        if abs(nxt - xk) < tol or abs(fv / dfv) < tol:
            return nxt, float(f.subs(var, nxt)), i
        xk = nxt
    return xk, float(f.subs(var, xk)), i


def iterate(expr, var, a, b, tol):
    f = expr
    df = der(f, var)
    d2f = der(df, var)
    if not (mono_up(f, a, b, var) or mono_down(f, a, b, var)):
        raise RuntimeError("Функция не монотонна")
    if float(f.subs(var, a) * d2f.subs(var, a)) > 0:
        xk = a
    elif float(f.subs(var, b) * d2f.subs(var, b)) > 0:
        xk = b
    else:
        xk = (a + b) / 2
    da = abs(float(df.subs(var, a)))
    db = abs(float(df.subs(var, b)))
    mu = max(da, db)
    lam = 1 / mu
    if mono_down(df, a, b, var):
        lam = -lam
    phi = var + lam * f
    dphi = der(phi, var)
    for xv in np.linspace(a, b, 100):
        if abs(float(dphi.subs(var, xv))) >= 1:
            raise RuntimeError("Не сходится")
    i = 0
    while True:
        i += 1
        nxt = float(phi.subs(var, xk))
        if abs(nxt - xk) < tol:
            return nxt, float(f.subs(var, nxt)), i
        xk = nxt


def newton_system(fun_sys, jac, start, tol):
    z = np.array(start, dtype=float)
    hist = []
    i = 0
    while True:
        i += 1
        Fz = fun_sys(z)
        Jz = jac(z)
        delta = np.linalg.solve(Jz, Fz)
        nxt = z - delta
        hist.append(np.abs(nxt - z))
        if np.all(np.abs(nxt - z) <= tol) and np.all(np.abs(fun_sys(nxt) - Fz) <= tol):
            return nxt, i, hist
        z = nxt


def plot_eq(fun, a, b, root=None):
    xs = np.linspace(a, b, 300)
    ys = np.array([fun(x) for x in xs])
    plt.figure()
    plt.plot(xs, ys, label="f(x)")
    plt.axhline(0, color='k', linewidth=0.5)
    if root is not None:
        plt.scatter(root, fun(root), c='g', zorder=5, label="Корень")
    plt.title("График")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_sys(fun_sys, xr, yr, root=None, title="Система"):
    xs = np.linspace(xr[0], xr[1], 300)
    ys = np.linspace(yr[0], yr[1], 300)
    X, Y = np.meshgrid(xs, ys)
    Z1 = np.zeros_like(X)
    Z2 = np.zeros_like(X)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            v = fun_sys([X[i, j], Y[i, j]])
            Z1[i, j], Z2[i, j] = v[0], v[1]
    plt.figure()
    plt.contour(X, Y, Z1, levels=[0], colors='b')
    plt.contour(X, Y, Z2, levels=[0], colors='r')
    if root is not None:
        plt.scatter(root[0], root[1], c='g', s=40, label="Решение")
    plt.title(title)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.legend()
    plt.show()


# ======================= ОСНОВНОЙ КОД =======================

def solve_single():
    # Три заранее заданных уравнения:
    # 1) x^3 + 2*x - 5
    # 2) cos(x) - x
    # 3) x^4 - 3*x + 1

    while True:
        print("Выберите одно из трёх уравнений:")
        print(" 1) x³ + 2·x − 5")
        print(" 2) cos(x) − x")
        print(" 3) x⁴ − 3·x + 1")
        ch = input("1..3: ").strip()
        if ch == '1':
            num_fun = lambda x: x**3 + 2*x - 5
            sym_x = sp.symbols('x')
            sym_fun = sp.sympify("x**3 + 2*x - 5")
            break
        elif ch == '2':
            num_fun = lambda x: np.cos(x) - x
            sym_x = sp.symbols('x')
            sym_fun = sp.sympify("cos(x) - x")
            break
        elif ch == '3':
            num_fun = lambda x: x**4 - 3*x + 1
            sym_x = sp.symbols('x')
            sym_fun = sp.sympify("x**4 - 3*x + 1")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

    # Ввод a, b, eps
    while True:
        print(" 1) Ввести a, b, ε с клавиатуры")
        print(" 2) Считать из файла")
        opt = input("Ваш выбор: ").strip()
        if opt == '1':
            vals = input_three()
            if vals:
                a, b, eps = vals
                break
        elif opt == '2':
            fn = input("Имя файла: ").strip()
            vals = load_three(fn)
            if vals:
                a, b, eps = vals
                break
            print("Неверные данные.")
        else:
            print("Нужно 1 или 2.")

    roots = count_roots(num_fun, a, b)
    if roots == 0:
        print("На этом отрезке корней нет.")
        return
    if roots > 1:
        print("Найдено несколько корней, сузьте интервал.")
        return

    while True:
        print("Выберите метод:")
        print(" 1) Секущие")
        print(" 2) Ньютон")
        print(" 3) Итерации")
        m = input("1..3: ").strip()
        if m in ('1', '2', '3'):
            break
        print("Повторите ввод.")

    try:
        if m == '1':
            root, fv, it = secant(num_fun, a, b, eps)
        elif m == '2':
            root, fv, it = newton_single(sym_fun, sym_x, a, b, eps)
        else:
            root, fv, it = iterate(sym_fun, sym_x, a, b, eps)
    except Exception as e:
        print("Ошибка решения:", e)
        return

    out = f"Корень: {root}\nf(корня): {fv}\nИтераций: {it}\n"
    while True:
        print(" 1) Показать результат")
        print(" 2) Записать в файл")
        o = input("1 или 2: ").strip()
        if o == '1':
            print(out)
            break
        elif o == '2':
            fn = input("Имя файла: ").strip()
            write_text(fn, out)
            break
        else:
            print("Неверно.")
    plot_eq(num_fun, a, b, root)


def solve_system():
    while True:
        print("Выберите систему:")
        print(" 1) x² + y² = 25; x² − y = 5")
        print(" 2) eˣ + y = 4; x + sin(y) = 1")
        choice = input("1 или 2: ").strip()
        if choice == '1':
            def f1(z):
                x, y = z[0], z[1]
                return np.array([x**2 + y**2 - 25, x**2 - y - 5])
            def j1(z):
                x, y = z[0], z[1]
                return np.array([[2*x, 2*y], [2*x, -1]])
            fun_sys, jac, title = f1, j1, "Система 1"
            break
        elif choice == '2':
            def f2(z):
                x, y = z[0], z[1]
                return np.array([np.exp(x) + y - 4, x + np.sin(y) - 1])
            def j2(z):
                x, y = z[0], z[1]
                return np.array([[np.exp(x), 1], [1, np.cos(y)]])
            fun_sys, jac, title = f2, j2, "Система 2"
            break
        else:
            print("Попробуйте снова.")

    while True:
        try:
            x0 = to_float(input("x₀ = "))
            y0 = to_float(input("y₀ = "))
            break
        except:
            print("Неверный ввод.")

    try:
        sol, it, hist = newton_system(fun_sys, jac, [x0, y0], 0.01)
    except Exception as e:
        print("Ошибка при решении:", e)
        return

    print(f"Решение: {sol}, Итераций: {it}")
    print("Погрешности:")
    for e in hist:
        print(e)

    xr = [sol[0] - 2, sol[0] + 2]
    yr = [sol[1] - 2, sol[1] + 2]
    plot_sys(fun_sys, xr, yr, sol, title)


def main_menu():
    while True:
        print(" 1) Решение одного уравнения")
        print(" 2) Решение системы")
        print(" q) Выход")
        cmd = input("Ваш выбор: ").strip().lower()
        if cmd == '1':
            solve_single()
        elif cmd == '2':
            solve_system()
        elif cmd == 'q':
            print("Выход.")
            sys.exit(0)
        else:
            print("Неверный ввод.")


if __name__ == '__main__':
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nЗавершение.")
