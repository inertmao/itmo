import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# --- Загрузка данных ---
data = pd.read_csv('kc_house_data.csv')

# --- Изучение цены ---
prices = data['price']

print("Описание цены:")
print(prices.describe())

plt.hist(prices, bins=50, edgecolor='black')
plt.title('Гистограмма распределения цены на недвижимость')
plt.xlabel('Цена')
plt.ylabel('Частота')
plt.show()

# --- Тест 1: Колмогоров-Смирнов на нормальность цены (свой) ---
def kolmogorov_smirnov_test(data_sample, cdf, args=()):
    n = len(data_sample)
    data_sorted = np.sort(data_sample)
    cdf_values = cdf(data_sorted, *args)
    
    D_plus = np.max(np.arange(1, n+1)/n - cdf_values)
    D_minus = np.max(cdf_values - np.arange(0, n)/n)
    D = max(D_plus, D_minus)
    
    alpha = 0.05
    D_critical = 1.36 / np.sqrt(n)
    
    p_value = stats.kstest(data_sample, cdf, args=args).pvalue
    
    return D, D_critical, p_value

prices_standardized = (prices - prices.mean()) / prices.std()

D, D_critical, p_value = kolmogorov_smirnov_test(prices_standardized, stats.norm.cdf)
print(f"\nКолмогоров-Смирнов (ручной): D = {D:.4f}, критическое = {D_critical:.4f}, p-value = {p_value:.4f}")
print("H0: цена распределена нормально")
print("Результат:", "Отвергаем H0" if D > D_critical else "Нет оснований отвергать H0")

# --- Тест 2: Колмогоров-Смирнов (готовый) ---
ks_stat, ks_pvalue = stats.kstest(prices_standardized, 'norm')
print(f"Колмогоров-Смирнов (scipy): D = {ks_stat:.4f}, p-value = {ks_pvalue:.4f}")

# --- Сравнение старого и нового фонда ---

# Добавим столбец возраста дома (текущий год 2023)
data['age'] = 2023 - data['yr_built']

# Разделим на старый (>30 лет) и новый фонд
old_fund = data[data['age'] > 30]['price']
new_fund = data[data['age'] <= 30]['price']

old_std = (old_fund - old_fund.mean()) / old_fund.std()
new_std = (new_fund - new_fund.mean()) / new_fund.std()

def ks_homogeneity_test(sample1, sample2):
    n1, n2 = len(sample1), len(sample2)
    data_all = np.sort(np.concatenate([sample1, sample2]))
    
    cdf1 = np.searchsorted(np.sort(sample1), data_all, side='right') / n1
    cdf2 = np.searchsorted(np.sort(sample2), data_all, side='right') / n2
    
    D = np.max(np.abs(cdf1 - cdf2))
    
    n = n1 * n2 / (n1 + n2)
    D_critical = 1.36 / np.sqrt(n)
    
    p_value = stats.ks_2samp(sample1, sample2).pvalue
    
    return D, D_critical, p_value

D, D_critical, p_value = ks_homogeneity_test(old_std, new_std)
print(f"\nТест однородности Колмогоров-Смирнова (ручной): D = {D:.4f}, критическое = {D_critical:.4f}, p-value = {p_value:.4f}")
print("H0: распределения цены одинаковы для старого и нового фонда")
print("Результат:", "Отвергаем H0" if D > D_critical else "Нет оснований отвергать H0")

res = stats.ks_2samp(old_std, new_std)
print(f"Тест KS (scipy): D = {res.statistic:.4f}, p-value = {res.pvalue:.4f}")

# --- Корреляция цены и жилой площади ---

x = data['sqft_living']
y = data['price']

def pearson_correlation(x, y):
    n = len(x)
    mean_x, mean_y = np.mean(x), np.mean(y)
    cov_xy = np.sum((x - mean_x) * (y - mean_y))
    std_x = np.sqrt(np.sum((x - mean_x)**2))
    std_y = np.sqrt(np.sum((y - mean_y)**2))
    r = cov_xy / (std_x * std_y)
    
    t_stat = r * np.sqrt((n - 2) / (1 - r**2))
    p_value = 2 * (1 - stats.t.cdf(abs(t_stat), df=n-2))
    
    return r, t_stat, p_value

r, t_stat, p_value = pearson_correlation(x, y)
print(f"\nКоэффициент корреляции Пирсона (ручной): r = {r:.4f}, t = {t_stat:.4f}, p-value = {p_value:.4f}")
print("H0: корреляция отсутствует")
print("Результат:", "Отвергаем H0" if p_value < 0.05 else "Нет оснований отвергать H0")

r_scipy, p_scipy = stats.pearsonr(x, y)
print(f"Коэффициент корреляции (scipy): r = {r_scipy:.4f}, p-value = {p_scipy:.4f}")

plt.scatter(x, y, alpha=0.3)
plt.title('Зависимость цены от жилой площади')
plt.xlabel('Жилая площадь (sqft_living)')
plt.ylabel('Цена')
plt.show()
