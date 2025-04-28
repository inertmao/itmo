import sys

"""
ВЫЧМАТ
Лабораторная работа 1
Исмоилов Шахзод
P3207 373296
Вариант 4
Метод простых итераций
"""

class IterationMethod:
    accuracy: float = 0.1
    size: int = 0
    matrix: list[list[float]] = []
    right_parts: list[float] = []
    MAX_ITERATION_COUNT = 1000

    def readMatrix(self) -> None:
        if len(sys.argv) == 3:
            try:
                with open(sys.argv[1], "r") as inp_file:
                    for line in inp_file.readlines():
                        self.matrix.append(list(map(float, line.strip().split(","))))
                self.size = len(self.matrix)
                # Проверка допустимых значений элементов
                for i, row in enumerate(self.matrix):
                    for j, value in enumerate(row):
                        if abs(value) > 1e6:
                            raise ValueError(f"❌ Значение слишком большое в позиции ({i+1}, {j+1}): {value}. Допустим максимум 1e6.")
                        if abs(value) < 1e-12 and j != self.size:  # Не проверяем свободный член
                            print(f"⚠️ Предупреждение: Очень маленький коэффициент в позиции ({i+1}, {j+1}) — возможна потеря точности.")


                # Проверка количества элементов в каждой строке
                for row in self.matrix:
                    if len(row) != self.size + 1:
                        raise ValueError("Неверное количество элементов в строке")

                while True:
                    try:
                        acc = float(sys.argv[2])
                        if acc <= 0:
                            print("Погрешность должна быть положительным числом. Введите заново:")
                            acc = float(input("Введите погрешность: "))
                        if acc > 0:
                            self.accuracy = acc
                            break
                    except ValueError:
                        print("Неверный формат. Введите число:")
                        sys.argv[2] = input("Введите погрешность: ")
            except Exception as e:
                print(f"Ошибка при чтении файла: {e}")
                print("Переключаюсь на ручной ввод матрицы.")
                self.manual_input()
        else:
            self.manual_input()

        for i in range(self.size):
            self.right_parts.append(self.matrix[i].pop())

    def manual_input(self):
        while True:
            try:
                self.accuracy = float(input("Введите погрешность: "))
                if self.accuracy <= 0:
                    print("Погрешность должна быть положительным числом. Попробуйте снова.")
                else:
                    break
            except ValueError:
                print("Введите корректное число.")

        while True:
            try:
                self.size = int(input("Введите количество строк: "))
                if self.size <= 0:
                    print("Количество строк должно быть положительным числом. Попробуйте снова.")
                else:
                    break
            except ValueError:
                print("Введите корректное целое число.")

        print("Вводите матрицу:")
        for i in range(self.size):
            while True:
                try:
                    row = list(map(float, input(f"Строка {i + 1}: ").split()))
                    if len(row) != self.size + 1:
                        print(f"Ошибка: ожидается {self.size + 1} чисел (включая свободный член). Попробуйте снова.")
                    else:
                        self.matrix.append(row)
                        break
                except ValueError:
                    print("Введите корректные числа.")

    def to_diag_dominance(self) -> None:
        for i in range(self.size):
            column_slice = self.get_column(i)[i:]
            if not column_slice:
                continue  # Пустой срез — пропускаем

            # Ищем элемент с максимальным модулем и его индекс в срезе
            max_index = max(range(len(column_slice)), key=lambda idx: abs(column_slice[idx]))
            line_index = i + max_index  # Смещение к глобальному индексу строки

            # Меняем строки местами
            self.matrix[i], self.matrix[line_index] = self.matrix[line_index], self.matrix[i]
            self.right_parts[i], self.right_parts[line_index] = self.right_parts[line_index], self.right_parts[i]



    def is_diag_dominance(self) -> bool:
        is_strictly = False
        for i in range(self.size):
            if self.matrix[i][i] > sum(map(abs, self.matrix[i])) - abs(self.matrix[i][i]):
                is_strictly = True
            elif self.matrix[i][i] < sum(map(abs, self.matrix[i])) - abs(self.matrix[i][i]):
                return False
        return is_strictly


    def solve(self) -> (list[float], int, list[float]):
        C = [[-1 * num / line[i] if i != j else 0
              for j, num in enumerate(line)]
             for i, line in enumerate(self.matrix)]
        D = [num / self.matrix[i][i] for i, num in enumerate(self.right_parts)]
        X = D.copy()
        iter_count = 0
        while True:
            print("Итерация ", iter_count)
            print("Значения X: ", X)
            iter_count += 1
            if iter_count > self.MAX_ITERATION_COUNT:
                print("Превышено максимальное количество итераций!", file=sys.stderr)
                sys.exit(1)
            X_next = [
                sum(self.mul_vectors(C[i], X)) + D[i]
                for i in range(self.size)
            ]
            if max(map(abs, self.sub_vectors(X_next, X))) < self.accuracy:
                r = []
                for i in range(len(self.matrix)):
                    r.append(sum(self.mul_vectors(self.matrix[i], X)) - self.right_parts[i])
                print("Критерий по невязке:")
                print(r)
                return X_next, iter_count, list(map(abs, self.sub_vectors(X_next, X)))
            X = X_next

    def get_column(self, i: int) -> list[float]:
        return [j[i] for j in self.matrix]

    def set_column(self, i: int, column: list[float]):
        for j in range(self.size):
            self.matrix[j][i] = column[j]

    def mul_vectors(self, list1: list[float], list2: list[float]) -> list[float]:
        return [list1[i] * list2[i] for i in range(len(list1))]

    def sub_vectors(self, list1: list[float], list2: list[float]):
        return [list1[i] - list2[i] for i in range(len(list1))]

    def print(self):
        for i, row in enumerate(self.matrix):
            for element in row:
                print("{:8}".format(element), end='')
            print("{:8}".format(self.right_parts[i]))


def main():
    solver = IterationMethod()
    solver.readMatrix()
    print("Получена матрица:")
    solver.print()
    if not solver.is_diag_dominance():
        solver.to_diag_dominance()
        print("Приведение к матрице преобладания диагональных коэффициентов:")
        solver.print()
        if not solver.is_diag_dominance():
            print("❌ Приведение к матрице преобладания диагональных коэффициентов невозможно. Метод простых итераций не гарантирует сходимость.", file=sys.stderr)
            sys.exit(1)  # Завершаем программу, чтобы не выполнять solve()


    if not solver.is_diag_dominance():
        print("⚠️ Внимание: матрица не обладает диагональным преобладанием. Метод может не сойтись.", file=sys.stderr)

    X, iter_count, acc_list = solver.solve()
    print("Вектор неизвестных:")
    print(X)
    print("Количество итераций: ", iter_count)
    print("Вектор погрешностей:")
    print(acc_list)



if __name__ == '__main__':
    main()
