import pandas as pd
import numpy as np
import scipy.stats as stats

# Загрузка данных
iris = pd.read_csv('iris .csv')

# Проверим названия столбцов
print(iris.columns)

# Создадим новую колонку — суммарная площадь чашелистика и лепестка
# Если имеется в виду сумма длины и ширины чашелистика и лепестка, то например:
# total_area = Sepal.Length * Sepal.Width + Petal.Length * Petal.Width
# ИЛИ просто сумма Sepal.Length + Petal.Length, уточни в условии
iris['TotalArea'] = iris['Sepal.Length'] * iris['Sepal.Width'] + iris['Petal.Length'] * iris['Petal.Width']

# Группировка по фактору — подвид
groups = [group['TotalArea'].values for name, group in iris.groupby('Species')]

# Размеры выборок
n_groups = [len(g) for g in groups]

# Общее число наблюдений
N = sum(n_groups)

# Общее среднее
grand_mean = np.mean(np.concatenate(groups))

# Межгрупповая сумма квадратов (SSB)
ssb = sum(n * (np.mean(g) - grand_mean)**2 for n, g in zip(n_groups, groups))

# Внутригрупповая сумма квадратов (SSW)
ssw = sum(sum((x - np.mean(g))**2 for x in g) for g in groups)

# Степени свободы
df_between = len(groups) - 1
df_within = N - len(groups)

# Средние квадраты
msb = ssb / df_between
msw = ssw / df_within

# Статистика F
F = msb / msw

# Критическое значение F (уровень значимости alpha=0.05)
alpha = 0.05
F_critical = stats.f.ppf(1 - alpha, df_between, df_within)

# P-value
p_value = 1 - stats.f.cdf(F, df_between, df_within)

print(f'F-statistic: {F:.4f}')
print(f'F-critical (alpha=0.05): {F_critical:.4f}')
print(f'p-value: {p_value:.4e}')

if F > F_critical:
    print('Отвергаем гипотезу о равенстве средних (есть статистически значимые различия)')
else:
    print('Нет оснований отвергать гипотезу о равенстве средних')
