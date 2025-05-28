# task1.py
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Параметры
mu1, mu2 = 2, 1
var1, var2 = 1, 0.5
tau_true = mu1 - mu2
alpha = 0.05
z_alpha = norm.ppf(1 - alpha/2)
n_list = [25, 10000]
n_simulations = 1000
np.random.seed(42)

# Эксперимент
plt.figure(figsize=(10, 6))
for idx, n in enumerate(n_list):
    coverage = 0
    ci_lower_list = []
    ci_upper_list = []
    std_dev = np.sqrt(var1/n + var2/n)
    
    for i in range(n_simulations):
        sample1 = np.random.normal(mu1, np.sqrt(var1), n)
        sample2 = np.random.normal(mu2, np.sqrt(var2), n)
        xbar1, xbar2 = np.mean(sample1), np.mean(sample2)
        tau_hat = xbar1 - xbar2
        
        margin = z_alpha * std_dev
        ci_lower = tau_hat - margin
        ci_upper = tau_hat + margin
        ci_lower_list.append(ci_lower)
        ci_upper_list.append(ci_upper)
        
        if ci_lower <= tau_true <= ci_upper:
            coverage += 1

    plt.subplot(2, 1, idx+1)
    colors = ['green' if (l <= tau_true <= u) else 'red' 
              for l, u in zip(ci_lower_list, ci_upper_list)]
    plt.hlines(y=range(n_simulations), xmin=ci_lower_list, 
               xmax=ci_upper_list, color=colors, alpha=0.4)
    plt.axvline(tau_true, color='blue', linestyle='--')
    plt.title(f'n = {n}: Coverage = {coverage/n_simulations:.3f}')
    plt.ylabel('Номер симуляции')

plt.xlabel('Доверительный интервал')
plt.tight_layout()
plt.savefig('task1_plot.png', dpi=300)
plt.show()
