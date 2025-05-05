import os
from validate_input import count_roots_on_interval, quation_solution, validate_roots
import numpy as np
import matplotlib.pyplot as plt
import math


def try_to_convert_to_int(number):
    try:
        number_float = float(number)
        if number_float.is_integer():
            return int(number_float)
        else:
            return number_float
    except ValueError:  
        return float(number)


def hand_input(quation, method):
    while True:    
        a = choose_left_interval()
        b = choose_right_interval(a)
        count_roots = count_roots_on_interval(quation, a, b, 0.001) 
        if not (validate_roots(count_roots)):
            continue
        break
    inaccuracy = choose_inaccuracy()
    return a, b, inaccuracy

def file_input(quation, method):
    current_working_directory = os.path.dirname(__file__)
    file_name = input("Введите относительный путь к вашему файлу\n")
    print()
    file_path = os.path.join(current_working_directory, file_name)
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    if len(lines) == 3:
        data = []
        for line in lines:
            try:
                var = line.replace(",", ".")
                var = float(var)
                var = try_to_convert_to_int(var)
                data.append(var)
            except ValueError:
                print("Некорректные данные в указанном файле")
                exit()

            except UnboundLocalError:
                print("Некорректные данные в указанном файле")
                exit()
            continue

        a = data[0]
        b = data[1]
        inaccuracy = data[2]
        print("Прочитано a = ", a, "b = ", b, "точность = ", inaccuracy)
        if(float(b) - float(a) - 0.00001 < 0):
            print("Правая граница должна быть больше левой границы!")
            exit()
        count_roots = count_roots_on_interval(quation, a, b, 0.001) 
        if not (validate_roots(count_roots)):
            exit()
    else:
        print("Некорректное количество строк в указанном файле")
        exit()
    return a, b, inaccuracy

def choose_inaccuracy():
    while True:
        try:
            inaccuracy = (
            input(
                "Введите точность: "
            ).replace(",", ".")
            )
            inaccuracy = float(inaccuracy)
            return try_to_convert_to_int(inaccuracy)
        except ValueError:
            print("Введено некорректное число")
            continue

        except UnboundLocalError:
            print("Введено некорректное число")
            continue

def input_selection(quation, method):
    while True:
        try:
            print("Выберите уравнение:")
            input_selection = int(
                input(
                    "1) Ввод вручную \n2) Ввод из файла\n"
                )
            )
            if input_selection in range(1, 3):
                break
            print("Некорректная команда")
            continue
        except ValueError:
            print("Введено некорректное значение")
            continue
    switch_command = {
        1: hand_input,
        2: file_input,
    }
    a, b, inaccuracy = switch_command.get(input_selection, exit)(quation, method)
    return a, b, inaccuracy

def choose_quation():
    while True:
        try:
            print("Выберите уравнение:")
            input_quation = int(
                input(
                    "1) x^2 - 3x + 2 \n2) x^3 + 2x^2 - 5\n3) cos(x) - x^2\n"
                )
            )
            if input_quation in range(1, 4):
                break
            print("Некорректная команда")
            continue
        except ValueError:
            print("Введено некорректное значение")
            continue
    return input_quation

def choose_system():
    while True:
        try:
            print("Выберите уравнение:")
            input_quation = int(
                input(
                    "1) 0.1x^2 +x + 0.2y^2 - 0.3\n   0.2x^2 + y + 0.1xy -0.7\n2) 3y^2+0.5x^2-x\n   sin(x)^2-y\n"
                )
            )
            if input_quation in range(1, 3):
                break
            print("Некорректная команда")
            continue
        except ValueError:
            print("Введено некорректное значение")
            continue
    return input_quation

def choose_method():
    while True:
        try:
            print("Выберите метод:")
            input_variant = int(
                input(
                    "1) Метод половинного деления\n2) Метод Ньютона\n3) Метод простой итерации\n"
                ).replace(",", ".")
            )
            if input_variant in range(1, 4):
                break
            print("Некорректная команда")
            continue
        except ValueError:
            print("Введено некорректное значение")
            continue
    return input_variant

def choose_system_method():
    while True:
        try:
            print("Выберите метод:")
            input_variant = int(
                input(
                    "1) Метод простой итерации\n"
                ).replace(",", ".")
            )
            if input_variant in range(1, 2):
                break
            print("Некорректная команда")
            continue
        except ValueError:
            print("Введено некорректное значение")
            continue
    return input_variant

def choose_left_interval():
    while True:
        try:
            interval = (
            input(
                "Введите левую границу интервала: "
            ).replace(",", ".")
            )
            interval = int(interval)
            return try_to_convert_to_int(interval)

        except ValueError:
            try:
                interval = try_to_convert_to_int(interval)
                return interval
            except ValueError:
                print("Введено некорректное число")
            continue

        except UnboundLocalError:
            print("Введено некорректное число")
            continue


def choose_right_interval(a):
    while True:
        try:
            interval = (
            input(
                "Введите правую границу интервала: "
            ).replace(",", ".")
            )
            if(float(interval) - float(a) - 0.00001 < 0):
                print("Правая граница должна быть больше левой границы!")
                continue
            interval = int(interval)
            return try_to_convert_to_int(interval)

        except ValueError:
            try:
                interval = try_to_convert_to_int(interval)
                return interval
            except ValueError:
                print("Введено некорректное число")
            continue

        except UnboundLocalError:
            print("Введено некорректное число")
            continue

def choose_x():
    while True:
        try:
            interval = (
            input(
                "Введите значение x: "
            ).replace(",", ".")
            )
            interval = int(interval)
            return try_to_convert_to_int(interval)

        except ValueError:
            try:
                interval = try_to_convert_to_int(interval)
                return interval
            except ValueError:
                print("Введено некорректное число")
            continue

        except UnboundLocalError:
            print("Введено некорректное число")
            continue


def choose_y():
    while True:
        try:
            interval = (
            input(
                "Введите значение y: "
            ).replace(",", ".")
            )
            interval = int(interval)
            return try_to_convert_to_int(interval)

        except ValueError:
            try:
                interval = try_to_convert_to_int(interval)
                return interval
            except ValueError:
                print("Введено некорректное число")
            continue

        except UnboundLocalError:
            print("Введено некорректное число")
            continue

def choose_output_format():
    while True:
        try:
            print("Выберите формат вывода:")
            input_variant = int(
                input(
                    "1) В консоль\n2) В файл\n"
                )
            )
            if input_variant in range(1, 3):
                break
            print("Некорректная команда")
            continue
        except ValueError:
            print("Введено некорректное значение")
            continue
    return input_variant

def output_data(solution, function, iterations, quation):
    input_variant = choose_output_format()
    switch_command = {
        1: output_in_console,
        2: output_in_file,
    }
    switch_command.get(input_variant, exit)(solution, function, iterations, quation)
    

def output_in_console(solution, function, iterations, quation):
    if function is None or math.isnan(function):
        print("Не сходится")
    else:
        print(f"Уравнение: {quation}  \nРешение: {solution} \nf({solution}) =  {function} \nИтерации: {iterations}")

def output_in_file(solution, function, iterations, quation):
    try:
        filename = input("Введите имя файла для сохранения данных: ")

        file_path = os.path.join('/home/inertmao/Desktop/itmo/itmo/C24S/2-compMath/Lab-2/solutions', filename)

        if not os.path.exists('/home/inertmao/Desktop/itmo/itmo/C24S/2-compMath/Lab-2/solutions'):
            os.makedirs('/home/inertmao/Desktop/itmo/itmo/C24S/2-compMath/Lab-2/solutions')

        with open(file_path, 'w') as file:
            file.write("Уравнение: " + str(quation) + '\n')
            file.write("Решение: " + str(solution) + '\n')
            file.write("f("+ str(solution)+ ") = " + str(function) + '\n')
            file.write("Итерации = " + str(iterations) + '\n')

        print(f"Значения переменных успешно записаны в файл: {file_path}")

    except FileNotFoundError:
        print("Указанный путь не существует.")
    except PermissionError:
        print("У вас нет прав на создание файла в этой директории.")
def draw_grapth(quation, function, a, b, ans_x = None, ans_y = None):
    x_values = np.linspace(a-a*0.3, b+b*0.3, 100)
    y_values = quation_solution(quation, x_values)

    # Построим график функции
    plt.plot(x_values, y_values, label=function, color='b')

    # Добавим заголовок и метки осей
    plt.title('График функции ' + function)
    plt.xlabel('x')
    plt.ylabel('f(x)')

    # Добавим сетку
    plt.grid(True)

    # Отобразим линии вспомогательных осей
    plt.axhline(0, color='black', linewidth=2)  # увеличиваем толщину линии оси x до 2
    plt.axvline(0, color='black', linewidth=0.5)

     # Если переданы координаты точки, добавим ее на график
    if ans_x is not None and ans_y is not None:
        plt.scatter(ans_x, ans_y, color='r')

    # Добавим легенду
    plt.legend()

    # Отобразим график
    plt.savefig('graph.png')
