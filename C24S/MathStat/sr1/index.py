import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

# Данные: медианные зарплаты (в тыс. руб.)
data = np.array([47.7, 49.5, 81.3, 49.2, 67.7, 56.6, 54.7, 78.0, 70.3, 83.0])
n = len(data)

# 1) Вариационный ряд (отсортированные данные)
variation_series = np.sort(data)

# Описательные статистики
mean = np.mean(data)
var_sample = np.var(data, ddof=1)       # Выборочная дисперсия (ddof=1)
var_biased = np.var(data, ddof=0)       # Несмещённая (точнее: с делением на n)
median = np.median(data)
q1 = np.percentile(data, 25)
q3 = np.percentile(data, 75)

# Логарифмы данных
log_data = np.log(data)
mean_log = np.mean(log_data)
var_log_sample = np.var(log_data, ddof=1)

print(f"Вариационный ряд: {variation_series}")
print(f"Среднее арифметическое: {mean:.3f}")
print(f"Выборочная дисперсия (s^2): {var_sample:.3f}")
print(f"Несмещённая дисперсия (tilde s^2): {var_biased:.3f}")
print(f"Медиана: {median:.3f}")
print(f"Первый квартиль (Q1): {q1:.3f}")
print(f"Третий квартиль (Q3): {q3:.3f}")
print(f"Среднее логарифмов: {mean_log:.3f}")
print(f"Выборочная дисперсия логарифмов: {var_log_sample:.3f}")

# 2) Оценка параметров логнормального распределения
# Оценки максимального правдоподобия для a и sigma^2 - это выборочные среднее и дисперсия логарифмов
a_hat = mean_log
sigma2_hat = var_log_sample
sigma_hat = np.sqrt(sigma2_hat)

print(f"Оценка параметра a (mean log): {a_hat:.3f}")
print(f"Оценка параметра sigma^2 (var log): {sigma2_hat:.3f}")

# 3) Информация Фишера для параметра a (для нормального распределения ln X)
Fisher_info = 1 / sigma2_hat
print(f"Информация Фишера для параметра a: {Fisher_info:.3f}")

# 4) R-эффективность (MSE) оценки a
MSE_a = sigma2_hat / n
print(f"Теоретическая MSE оценки a: {MSE_a:.5f}")

# 5) Проверка достаточности — теоретически, среднее логарифмов является достаточной статистикой (комментарий)

# 6) Доверительный интервал для параметра a при уровне 95%
alpha = 0.05
z = stats.norm.ppf(1 - alpha/2)
margin = z * sigma_hat / np.sqrt(n)
CI_lower = a_hat - margin
CI_upper = a_hat + margin
print(f"95% доверительный интервал для параметра a: [{CI_lower:.3f}, {CI_upper:.3f}]")

# Построение гистограммы и графика плотности логнормального распределения
x_vals = np.linspace(min(data)*0.8, max(data)*1.2, 1000)
pdf_vals = stats.lognorm.pdf(x_vals, s=sigma_hat, scale=np.exp(a_hat))

plt.figure(figsize=(10,5))
plt.hist(data, bins=6, density=True, alpha=0.6, color='g', label='Гистограмма выборки')
plt.plot(x_vals, pdf_vals, 'r-', lw=2, label='Плотность логнормального распределения')
plt.title('Гистограмма и плотность логнормального распределения')
plt.xlabel('Зарплата (тыс. руб.)')
plt.ylabel('Плотность')
plt.legend()
plt.grid(True)
plt.show()

# Эмпирическая функция распределения (ECDF)
sorted_data = np.sort(data)
ecdf = np.arange(1, n+1) / n

plt.figure(figsize=(10,5))
plt.step(sorted_data, ecdf, where='post', label='Эмпирическая функция распределения')
plt.title('Эмпирическая функция распределения')
plt.xlabel('Зарплата (тыс. руб.)')
plt.ylabel('F(x)')
plt.grid(True)
plt.legend()
plt.show()
