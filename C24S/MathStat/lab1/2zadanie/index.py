import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Параметры истинного нормального распределения
mu_истинное = 23.86
sigma2_истинное = 241.89
sigma_истинное = np.sqrt(sigma2_истинное)

# Список объёмов выборок и число симуляций
список_n = list(range(10, 110, 10))
M = 1000

# Генерация выборок и вычисление оценок
записи = []
for n in список_n:
    for _ in range(M):
        выборка = np.random.normal(loc=mu_истинное, scale=sigma_истинное, size=n)
        mu_оценка = выборка.mean()
        sigma2_оценка = выборка.var(ddof=1)
        записи.append({
            'n': n,
            'μ̂': mu_оценка,
            'σ̂²': sigma2_оценка
        })

df = pd.DataFrame(записи)

# Подсчёт описательных статистик для каждой оценки
результаты = []
for n in список_n:
    подгруппа = df[df['n'] == n]
    mu_vals = подгруппа['μ̂']
    s2_vals = подгруппа['σ̂²']
    
    mean_mu = mu_vals.mean()
    bias_mu = mean_mu - mu_истинное
    var_mu = mu_vals.var(ddof=1)
    mse_mu = var_mu + bias_mu**2
    
    mean_s2 = s2_vals.mean()
    bias_s2 = mean_s2 - sigma2_истинное
    var_s2 = s2_vals.var(ddof=1)
    mse_s2 = var_s2 + bias_s2**2
    
    результаты.append({
        'n': n,
        'Среднее μ̂': mean_mu,
        'Смещение μ̂': bias_mu,
        'Дисперсия μ̂': var_mu,
        'MSE μ̂': mse_mu,
        'Среднее σ̂²': mean_s2,
        'Смещение σ̂²': bias_s2,
        'Дисперсия σ̂²': var_s2,
        'MSE σ̂²': mse_s2
    })

df_summary = pd.DataFrame(результаты)

# Вывод таблицы в консоль
print("\n=== Статистика оценок μ̂ и σ̂² по объёму выборки ===")
print(df_summary.to_string(index=False))

# Визуализация распределений оценок μ̂ и σ̂²
for параметр, цвет_гист in [('μ̂', 'skyblue'), ('σ̂²', 'lightgreen')]:
    plt.figure(figsize=(16, 12))
    for idx, n in enumerate(список_n, 1):
        plt.subplot(3, 4, idx)
        данные = df[df['n'] == n][параметр]
        sns.histplot(данные, bins=20, stat='density', edgecolor='black', color=цвет_гист)
        sns.kdeplot(данные, linestyle='--', color=('red' if параметр=='μ̂' else 'darkgreen'))
        plt.title(f"{параметр}, n = {n}")
        plt.xlabel(параметр)
        plt.ylabel("Плотность")
    plt.suptitle(f"Гистограмма и KDE оценки {параметр} при разных n", fontsize=16, y=1.02)
    plt.tight_layout()
    plt.show()

