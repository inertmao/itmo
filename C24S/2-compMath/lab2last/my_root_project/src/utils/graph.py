import sys
import numpy as np
import matplotlib.pyplot as plt
from utils.calculator import Calculator
from utils.colorful_string import ColorfulString

class Graph:
    STEPS = 30

    def __init__(self, left: float, right: float, eq: int):
        # Проверка области определения для уравнения 2 (sqrt)
        if eq == 2:
            min_x = -6.0 / 23.9
            if left < min_x:
                ColorfulString.println(
                    f"Для уравнения 2 (√) левый конец должен быть ≥ {min_x:.6f}"
                )
                sys.exit(1)

        # Формируем сетку по X и вычисляем Y с обработкой ошибок
        xs = np.linspace(left, right, Graph.STEPS + 1)
        ys = []
        for x in xs:
            try:
                ys.append(Calculator.calculate_function(x, eq))
            except ValueError as e:
                ColorfulString.println(
                    f"Ошибка при вычислении функции в точке {x:.6f}: {e}"
                )
                sys.exit(1)

        # Рисуем график
        plt.figure()
        plt.plot(xs, ys, marker='o')
        plt.title("Graph")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.grid(True)
        fname = "graph.png"
        try:
            plt.savefig(fname)
        except Exception:
            ColorfulString.println("Не удалось сохранить график!")
            sys.exit(1)
        finally:
            plt.close()