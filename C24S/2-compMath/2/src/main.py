from read_write import *
import sympy as sp
from single_methods import *
from system_method import *
from plots import *

def main():
    while True:
        print("Выберите тип задачи:")
        print("1 - Нелинейное уравнение")
        print("2 - Система нелинейных уравнений")
        task_choice = input("Введите 1 или 2 (или 'q' для выхода): ").strip()
        
        if task_choice.lower() == 'q':
            break

        if task_choice == "1":
            while True:
                print("Выберите уравнение:")
                print("1 - f(x) = x^3 - 4x^2 + 5x - 2")
                print("2 - f(x) = x^4 - 5x^3 + 6x^2 + 4x - 8")
                print("3 - f(x) = sin(x) + cos(2x) - 0.5")
                print("4 - f(x) = x^20 + 2x^2 - 8x + 1")
                eq_choice = input("Введите номер: ").strip()

                if eq_choice == "1":
                    f = lambda x: x**3 - 4*x**2 + 5*x - 2
                    f_expr = sp.sympify("x**3 - 4*x**2 + 5*x - 2")
                    break
                elif eq_choice == "2":
                    f = lambda x: x**4 - 5*x**3 + 6*x**2 + 4*x - 8
                    f_expr = sp.sympify("x**4 - 5*x**3 + 6*x**2 + 4*x - 8")
                    break
                elif eq_choice == "3":
                    f = lambda x: sp.sin(x) + sp.cos(2*x) - 0.5
                    f_expr = sp.sympify("sin(x) + cos(2*x) - 0.5")
                    break
                elif eq_choice == "4":
                    f = lambda x: x**20 + 2*x**2 - 8*x + 1
                    f_expr = sp.sympify("x**20 + 2*x**2 - 8*x + 1")
                    break
                else:
                    print("Некорректный выбор, попробуйте снова.")

            
            while True:
                print("Выберите метод решения:")
                print("1 - Метод хорд")
                print("2 - Метод Ньютона")
                print("3 - Метод простой итерации")
                method_choice = input("Введите номер: ").strip()

                if method_choice in ["1", "2", "3"]:
                    break
                print("Некорректный выбор метода, попробуйте снова.")

           
            while True:
                print("Выберите способ ввода исходных данных:")
                print("1 - С клавиатуры")
                print("2 - Из файла")
                input_choice = input("Введите 1 или 2: ").strip()

                if input_choice == "1":
                    try:
                        a, b, eps = input_data(["Введите левую границу интервала a: ", 
                                                "Введите правую границу интервала b: ",
                                                "Введите точность eps: "])
                        break
                    except Exception as e:
                        print("Ошибка ввода:", e)
                        continue
                elif input_choice == "2":
                    filename = input("Введите имя файла для чтения данных: ").strip()
                    data = read_data_from_file(filename)
                    if data is not None and len(data) >= 3:
                        a, b, eps = data[0], data[1], data[2]
                        break
                    print("Некорректные данные в файле, попробуйте снова.")
                else:
                    print("Некорректный выбор, попробуйте снова.")

            
            sign_changes = count_sign_changes(f, a, b)
            if sign_changes == 0:
                print("На данном интервале корней не обнаружено. Попробуйте другой интервал.")
                continue
            elif sign_changes > 1:
                print("На данном интервале обнаружено несколько корней. Уточните границы.")
                continue

            
            try:
                if method_choice == "1":
                    root, f_val, iterations = chord_method(f, a, b, eps)
                elif method_choice == "2":
                    root, f_val, iterations = newton_single(f, a, b, eps)
                elif method_choice == "3":
                    root, f_val, iterations = simple_iteration(lambda x: sp.sympify(f(x)), a, b, eps)
            except Exception as e:
                print("Ошибка при решении уравнения:", e)
                continue

            
            output_str = (f"Найденный корень: {root}\n"
                          f"Значение функции в корне: {f_val}\n"
                          f"Число итераций: {iterations}\n")

            while True:
                print("Выберите способ вывода результатов:")
                print("1 - На экран")
                print("2 - В файл")
                output_choice = input("Введите 1 или 2: ").strip()

                if output_choice == "1":
                    print(output_str)
                    break
                elif output_choice == "2":
                    out_filename = input("Введите имя файла для записи результатов: ").strip()
                    write_results_to_file(out_filename, output_str)
                    break
                else:
                    print("Некорректный выбор, попробуйте снова.")

            plot_function(f, a, b, root)

        elif task_choice == "2":
            
            while True:
                print("Выберите систему уравнений:")
                print("1 - Система 1: x^2 + y^2 = 25, x^2 - y = 5")
                print("2 - Система 2: e^x + y = 4, x + sin(y) = 1")
                sys_choice = input("Введите 1 или 2: ").strip()

                if sys_choice == "1":
                    F, J, system_label = F1, J1, "Система 1"
                    break
                elif sys_choice == "2":
                    F, J, system_label = F2, J2, "Система 2"
                    break
                else:
                    print("Некорректный выбор, попробуйте снова.")

            
            while True:
                try:
                    x0 = parse_float(input("Введите начальное приближение для x: "))
                    y0 = parse_float(input("Введите начальное приближение для y: "))
                    break
                except Exception as e:
                    print("Ошибка ввода:", e)
                    continue

            z0 = np.array([x0, y0])
            try:
                root, iterations, errors = newton_system(F, J, z0, 0.01)
            except Exception as e:
                print("Ошибка при решении системы методом Ньютона:", e)
                continue

            print(f"Найденное решение: {root}\nКоличество итераций: {iterations}\nВектор погрешностей:")
            for i in errors:
                print(i)

            
            x_interval = [root[0] - 2, root[0] + 2]
            y_interval = [root[1] - 2, root[1] + 2]
            plot_system(F, x_interval, y_interval, root, system_label)

        else:
            print("Некорректный выбор, попробуйте снова.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nВыход...")
