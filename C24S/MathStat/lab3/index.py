import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Загрузка данных
df = pd.read_csv('kc_house_data.csv')

# 1. Проверка распределения цены — логнормальное
prices = df['price'].values

shape, loc, scale = stats.lognorm.fit(prices, floc=0)

def ks_test(data, cdf, args=()):
    n = len(data)
    data_sorted = np.sort(data)
    cdf_vals = cdf(data_sorted, *args)
    d_plus = np.max(np.arange(1, n+1)/n - cdf_vals)
    d_minus = np.max(cdf_vals - (np.arange(0, n)/n))
    D = max(d_plus, d_minus)
    en = np.sqrt(n)
    p_value = stats.kstwobign.sf(D * en)
    return D, p_value

cdf_lognorm = lambda x, s, loc, scale: stats.lognorm.cdf(x, s, loc, scale)

D_ks, p_ks = ks_test(prices, cdf_lognorm, (shape, loc, scale))
alpha = 0.05
crit_val = 1.36 / np.sqrt(len(prices))

observed_freq, bin_edges = np.histogram(prices, bins=20)
expected_freq = []
for i in range(len(bin_edges)-1):
    expected_freq.append(
        len(prices) * (stats.lognorm.cdf(bin_edges[i+1], shape, loc, scale) - stats.lognorm.cdf(bin_edges[i], shape, loc, scale))
    )
expected_freq = np.array(expected_freq)

chi2_stat = ((observed_freq - expected_freq) ** 2 / expected_freq).sum()
df_chi = len(observed_freq) - 1 - 3
p_chi = 1 - stats.chi2.cdf(chi2_stat, df_chi)

print(f"KS-test вручную: D = {D_ks:.4f}, p-value = {p_ks:.4e}")
print(f"Критическое значение KS: {crit_val:.4f}")
print(f"Chi2-test: chi2 = {chi2_stat:.2f}, p-value = {p_chi:.4e}")

print("\n1. Проверка распределения цены:")
if p_ks > alpha:
    print(f"- KS-тест не отвергает гипотезу о логнормальном распределении (p={p_ks:.4e} > {alpha})")
else:
    print(f"- KS-тест отвергает гипотезу (p={p_ks:.4e} <= {alpha})")

if p_chi > alpha:
    print(f"- Chi2-тест не отвергает гипотезу о логнормальном распределении (p={p_chi:.4e} > {alpha})")
else:
    print(f"- Chi2-тест отвергает гипотезу (p={p_chi:.4e} <= {alpha})")

# Построение гистограммы с наложением логнормального PDF
plt.figure(figsize=(8,6))
count, bins, ignored = plt.hist(prices, bins=20, density=True, alpha=0.6, color='g', label='Гистограмма цены')
x = np.linspace(min(prices), max(prices), 1000)
pdf = stats.lognorm.pdf(x, shape, loc, scale)
plt.plot(x, pdf, 'r-', lw=2, label='Логнормальное распределение')
plt.title('Гистограмма цены с логнормальным распределением')
plt.xlabel('Цена')
plt.ylabel('Плотность вероятности')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('price_histogram.png')
plt.close()

# 2. Проверяем равенство распределений цены старого и нового фонда
df['old'] = df['yr_built'] <= (df['yr_built'].max() - 30)
prices_old = df[df['old'] == True]['price'].values
prices_new = df[df['old'] == False]['price'].values

ks_stat, ks_pval = stats.ks_2samp(prices_old, prices_new)
print(f"\n2. Проверка равенства распределений цены (KS тест scipy): D = {ks_stat:.4f}, p = {ks_pval:.4e}")

obs_old, bins = np.histogram(prices_old, bins=20)
obs_new, _ = np.histogram(prices_new, bins=bins)

total_sum = (obs_old.sum() + obs_new.sum()) / 2
obs_old_norm = obs_old / obs_old.sum() * total_sum
obs_new_norm = obs_new / obs_new.sum() * total_sum

eps = 1e-10
mask = (obs_new_norm > eps) & (obs_old_norm > eps)

obs_old_filtered = obs_old_norm[mask]
obs_new_filtered = obs_new_norm[mask]

sum_old = obs_old_filtered.sum()
sum_new = obs_new_filtered.sum()
mean_sum = (sum_old + sum_new) / 2

obs_old_filtered = obs_old_filtered / sum_old * mean_sum
obs_new_filtered = obs_new_filtered / sum_new * mean_sum

chi2_2, pval_2 = stats.chisquare(f_obs=obs_old_filtered, f_exp=obs_new_filtered)
print(f"Chi2-тест (нормированный и отфильтрованный): chi2 = {chi2_2:.2f}, p = {pval_2:.4e}")

if ks_pval > alpha:
    print("- KS тест не отвергает гипотезу о равенстве распределений")
else:
    print("- KS тест отвергает гипотезу о равенстве распределений")

if pval_2 > alpha:
    print("- Chi2 тест не отвергает гипотезу о равенстве распределений")
else:
    print("- Chi2 тест отвергает гипотезу о равенстве распределений")

# 3. Корреляция площади и цены
sqft = df['sqft_living'].values

x = sqft
y = prices
n = len(x)
mean_x = np.mean(x)
mean_y = np.mean(y)
cov_xy = np.sum((x - mean_x) * (y - mean_y)) / n
std_x = np.std(x)
std_y = np.std(y)
r = cov_xy / (std_x * std_y)

t_stat = r * np.sqrt((n - 2) / (1 - r**2))
p_corr = 2 * (1 - stats.t.cdf(abs(t_stat), df=n-2))
print(f"\n3. Корреляция Пирсона (вручную): r = {r:.4f}, t = {t_stat:.4f}, p = {p_corr:.4e}")

spearman_rho, spearman_p = stats.spearmanr(x, y)
print(f"Корреляция Спирмена (scipy): rho = {spearman_rho:.4f}, p = {spearman_p:.4e}")

if p_corr < alpha:
    print("- Отвергаем H0, существует значимая корреляция между площадью и ценой")
else:
    print("- Не отвергаем H0, значимой корреляции нет")

# Построение графика зависимости цены от площади
plt.figure(figsize=(8,6))
plt.scatter(sqft, prices, s=10, alpha=0.3)
plt.title("Зависимость цены от жилой площади")
plt.xlabel("Площадь жилой части (кв.футы)")
plt.ylabel("Цена")
plt.grid(True)
plt.tight_layout()
plt.savefig('price_vs_sqft.png')
plt.close()

