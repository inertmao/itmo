import matplotlib.pyplot as plt

def plot_all(x, y, lag, newt, fwd=None, bwd=None, x0=None, vals=None, real=None):
    xs = [min(x) + i*(max(x)-min(x))/1000 for i in range(1001)]
    ys_lag = [lag(xi) for xi in xs]
    ys_newt = [newt(xi) for xi in xs]

    plt.figure()
    if real:
        ys_real = [real(xi) for xi in xs]
        plt.plot(xs, ys_real, label="Функция")

    plt.plot(xs, ys_lag, "--", label="Лагранж")
    plt.plot(xs, ys_newt, "-.", label="Ньютон (разд.)")

    if fwd:
        ys_fwd = [fwd(xi) for xi in xs]
        plt.plot(xs, ys_fwd, ":", label="Ньютон (вперёд)")
    if bwd:
        ys_bwd = [bwd(xi) for xi in xs]
        plt.plot(xs, ys_bwd, ":", label="Ньютон (назад)")

    plt.plot(x, y, "o", label="Узлы")
    plt.legend()
    plt.title("Интерполяция")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()
