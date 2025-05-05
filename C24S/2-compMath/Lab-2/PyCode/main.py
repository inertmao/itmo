from non_lineare_quation import *
from non_lineare_system import *
while True:
    try:
        print("Выберите вариант:")
        input_variant = int(
            input(
                "1) Нелинейное уравнение\n2) Система нелинейных уравнений\n"
            )
        )
        if input_variant in range(1, 3):
            switch_command = {
                1: non_lineare_quation,
                2: non_lineare_system,
                3: exit,
            }
            switch_command.get(input_variant, exit)()
        else:
            print("Некорректный вариант")
            continue
    except ValueError:
        print("Введено некорректное значение")
        continue
    except Exception:
        print("Что-то пошло не так")
        continue