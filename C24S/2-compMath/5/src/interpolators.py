def lagrange(x, y):
    def poly(x0):
        res = 0.0
        n = len(x)
        for i in range(n):
            term = y[i]
            for j in range(n):
                if i != j:
                    term *= (x0 - x[j]) / (x[i] - x[j])
            res += term
        return res
    return poly

def div_diffs(x, y):
    n = len(x)
    tab = [row[:] for row in [y] + [[0]*n for _ in range(n-1)]]
    for lvl in range(1, n):
        for i in range(n-lvl):
            tab[lvl][i] = (tab[lvl-1][i+1] - tab[lvl-1][i]) / (x[i+lvl] - x[i])
    return tab

def newton_coef(x, y):
    tab = div_diffs(x, y)
    return [tab[i][0] for i in range(len(x))]

def newton(x, coef):
    def poly(x0):
        res = coef[0]
        for i in range(1, len(coef)):
            term = coef[i]
            for j in range(i):
                term *= (x0 - x[j])
            res += term
        return res
    return poly

def fwd_newton(x, y, x0):
    n = len(y)
    h = x[1] - x[0]
    diffs = [y[:]]
    for lvl in range(1, n):
        prev = diffs[lvl-1]
        diffs.append([prev[i+1] - prev[i] for i in range(n-lvl)])
    t = (x0 - x[0]) / h
    res = diffs[0][0]
    prod = 1.0
    for i in range(1, n):
        prod *= (t - (i-1)) / i
        res += prod * diffs[i][0]
    return res

def bwd_newton(x, y, x0):
    n = len(y)
    h = x[1] - x[0]
    diffs = [y[:]]
    for lvl in range(1, n):
        prev = diffs[lvl-1]
        diffs.append([prev[i+1] - prev[i] for i in range(n-lvl)])
    t = (x0 - x[-1]) / h
    res = diffs[0][-1]
    prod = 1.0
    for i in range(1, n):
        prod *= (t + (i-1)) / i
        res += prod * diffs[i][-1]
    return res
