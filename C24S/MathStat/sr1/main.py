import numpy as np
import scipy.stats as stats

# Параметры распределения Лапласа
beta = 2.0  # Пример
n = 1000

# Генерация выборки Лапласа с параметром beta
data = np.random.laplace(loc=0, scale=1/beta, size=n)

# Вычисление статистики
X_bar = np.mean(data)
stat = abs(X_bar)

# Оценка 1/beta
theta_hat = stat

# Смещённость
expected_stat = np.mean(np.abs(np.mean(np.random.laplace(0, 1/beta, (10000, n)), axis=1)))
bias = expected_stat - 1/beta

# Состоятельность проверяется теоретически

# Асимптотическая нормальность — по ЦПТ
var_X = 2 / (beta**2)  # дисперсия Лапласа
var_stat = var_X / n   # приблизительная дисперсия для X_bar
std_stat = np.sqrt(var_stat)

# Доверительный интервал
alpha = 0.05
z = stats.norm.ppf(1 - alpha/2)
CI_lower = stat - z * std_stat
CI_upper = stat + z * std_stat

print(f"Статистика |X̄|: {stat:.4f}")
print(f"Смещённость: {bias:.4f}")
print(f"Приблизительная дисперсия статистики: {var_stat:.6f}")
print(f"95% доверительный интервал: [{CI_lower:.4f}, {CI_upper:.4f}]")
