import numpy as np

def parse_float(user_input):
    try:
        return float(user_input.replace(',', '.'))
    except Exception as e:
        raise ValueError("Некорректное число: " + user_input)

def input_data(prompt_list):
    data = []
    for prompt in prompt_list:
        user_input = input(prompt)
        data.append(parse_float(user_input))
    return data

def read_data_from_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
        data = []
        if len(lines) == 1:
            data = [parse_float(x) for x in lines[0].split()]
        else:
            for line in lines:
                line = line.strip()
                if line:
                    data.append(parse_float(line))
        return data
    except Exception as e:
        print("Ошибка при чтении файла:", e)
        return None

def write_results_to_file(filename, results):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(results)
    except Exception as e:
        print("Ошибка при записи в файл:", e)