import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import scipy.stats as stats

# Загрузка данных
data = pd.read_csv('cars93.csv')

# Выбор нужных столбцов
# Предполагаем, что в данных столбцы названы: Price, CityMPG, HighwayMPG, Horsepower
# Проверим названия столбцов:
print(data.columns)

# Переименуем или адаптируем в зависимости от реальных названий
# Например:
# 'Price' — цена
# 'CityMPG' — расход в городе
# 'HighwayMPG' — расход на шоссе
# 'Horsepower' — мощность

# Если есть пропуски, удалим их
data = data[['Price', 'MPG.city', 'MPG.highway', 'Horsepower']].dropna()

# Если названия расхода на шоссе 'HighMPG' (проверьте после вывода), исправим при необходимости

# Независимые переменные
X = data[['MPG.city', 'MPG.highway', 'Horsepower']]
X = sm.add_constant(X)
y = data['Price']

# Построение модели
model = sm.OLS(y, X).fit()

# Коэффициенты
print(model.summary())

# Доверительные интервалы для коэффициентов
conf_int = model.conf_int()

# Остаточная дисперсия (mean squared error)
resid_var = model.mse_resid

# Коэффициент детерминации
r_squared = model.rsquared

# Проверка гипотезы H0: коэффициенты при CityMPG и HighMPG равны 0
hypothesis = ['MPG.city = 0', 'MPG.highway = 0']
f_test = model.f_test(hypothesis)
print(f_test)


# Проверка нормальности остатков (Shapiro-Wilk)
shapiro_test = stats.shapiro(model.resid)

# Построение графика: реальные и предсказанные значения
plt.figure(figsize=(8,6))
plt.scatter(y, model.fittedvalues, alpha=0.7)
plt.plot([y.min(), y.max()], [y.min(), y.max()], 'r--')
plt.xlabel('Реальная цена')
plt.ylabel('Предсказанная цена')
plt.title('Реальная vs. Предсказанная цена авто')
plt.grid(True)
plt.show()
