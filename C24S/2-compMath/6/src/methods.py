import math

def euler(f, x0, y0, h, n):
    xs = [x0]
    ys = [y0]
    for _ in range(n):
        x, y = xs[-1], ys[-1]
        yn = y + h * f(x, y)
        xn = x + h
        xs.append(xn)
        ys.append(yn)
    return xs, ys

def rk4(f, x0, y0, h, n):
    xs = [x0]
    ys = [y0]
    for _ in range(n):
        x, y = xs[-1], ys[-1]
        k1 = f(x, y)
        k2 = f(x + h/2, y + h*k1/2)
        k3 = f(x + h/2, y + h*k2/2)
        k4 = f(x + h, y + h*k3)
        yn = y + (h/6) * (k1 + 2*k2 + 2*k3 + k4)
        xn = x + h
        xs.append(xn)
        ys.append(yn)
    return xs, ys

def adams(f, x0, y0, h, n, exact):
    xs = [x0]
    ys = [y0]

    # если шагов меньше 3 → считаем только RK4
    if n < 3:
        for _ in range(n):
            x, y = xs[-1], ys[-1]
            k1 = f(x, y)
            k2 = f(x + h/2, y + h*k1/2)
            k3 = f(x + h/2, y + h*k2/2)
            k4 = f(x + h, y + h*k3)
            yn = y + (h/6) * (k1 + 2*k2 + 2*k3 + k4)
            xn = x + h
            xs.append(xn)
            ys.append(yn)
        real = [exact(xi) for xi in xs]
        errs = [abs(real[i] - ys[i]) for i in range(len(ys))]
        return xs, ys, max(errs)

    # первые 3 шага считаем RK4
    for _ in range(3):
        x, y = xs[-1], ys[-1]
        k1 = f(x, y)
        k2 = f(x + h/2, y + h*k1/2)
        k3 = f(x + h/2, y + h*k2/2)
        k4 = f(x + h, y + h*k3)
        yn = y + (h/6) * (k1 + 2*k2 + 2*k3 + k4)
        xn = x + h
        xs.append(xn)
        ys.append(yn)

    # остальные шаги методом Адамса
    for i in range(3, n):
        xi = xs[i]
        f0 = f(xs[i], ys[i])
        f1 = f(xs[i-1], ys[i-1])
        f2 = f(xs[i-2], ys[i-2])
        f3 = f(xs[i-3], ys[i-3])

        # предиктор
        yp = ys[i] + (h/24) * (55*f0 - 59*f1 + 37*f2 - 9*f3)
        xn = xi + h

        # корректор
        fp = f(xn, yp)
        yc = ys[i] + (h/24) * (9*fp + 19*f0 - 5*f1 + f2)

        xs.append(xn)
        ys.append(yc)

    # гарантируем одинаковую длину (n+1)
    xs = xs[:n+1]
    ys = ys[:n+1]

    # считаем погрешность
    real = [exact(xi) for xi in xs]
    errs = [abs(real[i] - ys[i]) for i in range(len(ys))]
    return xs, ys, max(errs)
