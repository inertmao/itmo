import sys
import math
from datasources import read_keyboard, read_file, read_func
from interpolators import lagrange, newton_coef, newton, fwd_newton, bwd_newton
from difference_table import print_table, print_divided
from plotter import plot_all

def main():
    try:
        while True:
            print("Источник данных (1-клав, 2-файл, 3-ф-я, q-выход):")
            ch = input().strip().lower()
            if ch == 'q':
                break
            if ch == '1':
                x, y = read_keyboard(); real=None
            elif ch == '2':
                x, y = read_file(); real=None
            elif ch == '3':
                x, y = read_func()
                real = math.sin if abs(y[1]-math.sin(x[1]))<1e-6 else math.cos
            else:
                print("Неверный выбор."); continue

            if len(x)<2 or len(set(x))!=len(x):
                print("Нужно ≥2 узлов и x уникальны."); continue

            h = x[1]-x[0]
            eq = all(abs((x[i+1]-x[i])-h)<1e-8 for i in range(len(x)-1))
            print()
            if eq:
                print("Таблица конечных разностей:")
                print_table(x,y)
            else:
                print("Таблица разделенных разностей:")
                print_divided(x,y)

            try:
                x0=float(input("\nВведите x0: ").replace(',','.'))
            except KeyboardInterrupt:
                raise
            except:
                print("Ошибка ввода."); continue

            lag = lagrange(x,y)
            coefs = newton_coef(x,y)
            newt = newton(x,coefs)

            r_lag = lag(x0)
            r_newt = newt(x0)
            vals = {'lag':r_lag,'newt':r_newt}

            print(f"Lagrange: {r_lag:.6f}")
            print(f"Newton(div): {r_newt:.6f}")

            fwd,bwd=None,None
            if eq:
                mid = (x[0]+x[-1])/2
                if x0<=mid:
                    fwd = lambda z: fwd_newton(x,y,z)
                    vals['fwd'] = fwd_newton(x,y,x0)
                    print(f"Newton fwd: {vals['fwd']:.6f}")
                else:
                    bwd = lambda z: bwd_newton(x,y,z)
                    vals['bwd'] = bwd_newton(x,y,x0)
                    print(f"Newton bwd: {vals['bwd']:.6f}")

            print("Рисую график... ")
            plot_all(x,y,lag,newt,fwd,bwd,x0,vals,real)
    except KeyboardInterrupt:
        print("\nВыход."); sys.exit(0)

if __name__=='__main__':
    main()
