import math
import numpy as np
import matplotlib.pyplot as plt
import traceback

def lin_pow(tab):
    x, y = tab
    try:
        for i in range(len(x)):
            x[i] = math.log(x[i])
        for j in range(len(y)):
            y[j] = math.log(y[j])
    except ValueError:
        raise ValueError("Ошибка: только положительные числа для степенной")
    return [x, y]

def lin_exp(tab):
    y = tab[1]
    try:
        for j in range(len(y)):
            y[j] = math.log(y[j])
    except ValueError:
        raise ValueError("Ошибка: только положительные числа для экспоненты")
    return tab

def lin_log(tab):
    x = tab[0]
    try:
        for i in range(len(x)):
            x[i] = math.log(x[i])
    except ValueError:
        raise ValueError("Ошибка: только положительные числа для логарифма")
    return tab

perms = 0

import pdb

def gauss(a, b):
    n = len(a)
    x = [0]*n

    for i in range(n-1):
        if abs(a[i][i]) < 1e-12:
            raise ZeroDivisionError("Метод Гаусса: нулевой диагональный элемент")
        for k in range(i+1, n):
            c = a[k][i] / a[i][i]
            a[k][i] = 0
            for j in range(i+1, n):
                a[k][j] -= c*a[i][j]
            b[k] -= c*b[i]

    for i in range(n-1, -1, -1):
        s = 0
        for j in range(i+1, n):
            s += a[i][j]*x[j]
        if abs(a[i][i]) < 1e-12:
            raise ZeroDivisionError("Метод Гаусса: деление на ноль")
        x[i] = (b[i]-s)/a[i][i]
    return x



def swap(a, i, b):
    global perms
    l = i
    n = len(a)
    for m in range(i+1, n):
        if abs(a[m][i]) > abs(a[l][i]):
            l = m
    if l != i:
        a[i], a[l] = a[l], a[i]
        b[i], b[l] = b[l], b[i]
        perms += 1

def min_sq(x, y, m):
    n = len(x)
    sum_x = []
    sum_y = []

    for p in range(m*2+1):
        sum_x.append(sum(xx**p for xx in x))

    for i in range(m+1):
        sum_y.append(sum((xx**i)*yy for xx,yy in zip(x,y)))
    a = sym_mat(sum_x, m)
    b = sum_y
    return gauss(a, b)

def sym_mat(arr, m):
    return [[arr[i+j] for j in range(m+1)] for i in range(m+1)]

def phi_poly(c, m):
    return lambda x: sum(c[i]*x**i for i in range(m+1))

def phi_pow(c):
    a,b = c
    return lambda x: a*x**b

def phi_exp(c):
    a,b = c
    return lambda x: a*math.exp(b*x)

def phi_log(c):
    a,b = c
    return lambda x: a + b*math.log(x)

def S(phi, tab):
    x,y = tab
    return sum((phi(x[i])-y[i])**2 for i in range(len(x)))

def MSE(phi, tab):
    return math.sqrt(S(phi,tab)/len(tab[0]))

def eps_arr(phi, tab):
    x,y = tab
    return [phi(x[i])-y[i] for i in range(len(x))]

def phi_arr(phi, x):
    return [phi(xx) for xx in x]

def det(phi, tab):
    y = tab[1]
    n = len(y)
    mse = MSE(phi, tab)
    phi_i = phi_arr(phi, tab[0])
    avg = sum(phi_i)/n
    den = sum((yy-avg)**2 for yy in y)
    return 1 - mse/den

def fmt(arr, p=3):
    return "["+", ".join(f"{x:.{p}f}" for x in arr)+"]"

def read_table(src=None):
    if src is None:
        x = read_line(input("x:\n"))
        y = read_line(input("y:\n"))
    else:
        with open(src,'r',encoding='utf-8') as f:
            lines = f.readlines()
        if len(lines)<2:
            raise ValueError("Файл должен иметь хотя бы 2 строки")
        x = read_line(lines[0])
        y = read_line(lines[1])
    if len(x)!=len(y):
        raise ValueError("Длины x и y не совпадают")

    # 🔹 проверка на одинаковые значения
    # if len(set(x)) == 1:
    #     raise ValueError("Ошибка: все значения x одинаковые, аппроксимация невозможна")
    # if len(set(y)) == 1:
    #     print("⚠️ Предупреждение: все значения y одинаковые, аппроксимация выродится в константу")

    return [x,y]

def read_line(s):
    arr = list(map(float, s.replace(',','.').split()))
    if not (8<=len(arr)<=12):
        raise ValueError("Количество точек 8–12")
    return arr

def print_res(name, c, mse, phi_i, eps, r2):
    print(name)
    print("Коэф.:", fmt(c))
    print(f"СКО: {mse:.3f}")
    print("φ(x):", fmt(phi_i))
    print("ε:", fmt(eps))
    print(f"R^2: {r2:.3f}\n")

def plot_all(tab, c_lin=None,c_p2=None,c_p3=None,c_exp=None,c_log=None,c_pow=None):
    x = np.array(tab[0])
    y = np.array(tab[1])
    xd = np.linspace(min(x), max(x), 300)

    plt.figure()
    plt.scatter(x,y,color='black',label="точки")

    if c_lin:
        plt.plot(xd, c_lin[0]+c_lin[1]*xd, label="Лин", lw=2)
    if c_p2:
        plt.plot(xd, c_p2[0]+c_p2[1]*xd+c_p2[2]*xd**2, label="Пол2", lw=2)
    if c_p3:
        plt.plot(xd, c_p3[0]+c_p3[1]*xd+c_p3[2]*xd**2+c_p3[3]*xd**3, label="Пол3", lw=2)
    if c_exp:
        plt.plot(xd, c_exp[0]*np.exp(c_exp[1]*xd), label="Эксп", lw=2)
    if c_log:
        xd_pos = xd[xd>0]
        if len(xd_pos)>0:
            plt.plot(xd_pos, c_log[0]+c_log[1]*np.log(xd_pos), label="Лог", lw=2)
    if c_pow:
        xd_pos = xd[xd>0]
        if len(xd_pos)>0:
            plt.plot(xd_pos, c_pow[0]*xd_pos**c_pow[1], label="Степ", lw=2)

    plt.legend()
    plt.grid()
    plt.show()

def main():
    while True:
        s = input("Ввод: 1 - ручной, 2 - файл\n")
        try:
            if s=='1':
                tab = read_table()
            elif s=='2':
                fname = input("Файл:\n")
                tab = read_table(fname)
            else:
                continue
        except Exception as e:
            print(e); continue

        try:
            c_lin = min_sq(tab[0],tab[1],1)
            c_p2 = min_sq(tab[0],tab[1],2)
            c_p3 = min_sq(tab[0],tab[1],3)
        except:
            print("Ошибка метода наименьших квадратов"); 
            
            continue
            

        c_exp = [math.exp(c_lin[0]), c_lin[1]]
        c_pow = [math.exp(c_lin[0]), c_lin[1]]
        c_log = c_lin

        models = {
            "Лин": (phi_poly(c_lin,1), c_lin),
            "Пол2": (phi_poly(c_p2,2), c_p2),
            "Пол3": (phi_poly(c_p3,3), c_p3),
            "Эксп": (phi_exp(c_exp), c_exp),
            "Лог": (phi_log(c_log), c_log),
            "Степ": (phi_pow(c_pow), c_pow)
        }

        out = input("Вывод: 1 - консоль, 2 - файл\n")
        if out=='1':
            for name,(phi,c) in models.items():
                try:
                    print_res(name,c,MSE(phi,tab),
                              phi_arr(phi,tab[0]),eps_arr(phi,tab),det(phi,tab))
                except Exception as e:
                    print(e)
        elif out=='2':
            fname = input("Файл:\n")
            with open(fname,'w',encoding='utf-8') as f:
                for name,(phi,c) in models.items():
                    try:
                        f.write(name+"\n")
                        f.write("Коэф.: "+fmt(c)+"\n")
                        f.write(f"СКО: {MSE(phi,tab):.3f}\n\n")
                    except: pass

        # выбор лучшей
        best = None; min_err=float('inf')
        for name,(phi,c) in models.items():
            try:
                e = MSE(phi,tab)
                if e<min_err:
                    min_err=e; best=(name,phi)
            except: pass
        if best:
            r2 = det(best[1],tab)
            print(f"Лучшая: {best[0]}, MSE={min_err:.3f}, R^2={r2:.3f}")

        plot_all(tab,c_lin,c_p2,c_p3,c_exp,c_log,c_pow)

if __name__=="__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Выход...")
