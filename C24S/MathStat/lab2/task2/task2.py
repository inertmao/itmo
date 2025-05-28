# task2.py
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import poisson, norm

# Параметры
lambda_true = 1
tau_true = lambda_true + lambda_true**2
alpha = 0.05
z_alpha = norm.ppf(1 - alpha/2)
n_list = [25, 10000]
n_simulations = 1000
np.random.seed(42)

plt.figure(figsize=(10, 6))
for idx, n in enumerate(n_list):
    coverage = 0
    ci_lower_list = []
    ci_upper_list = []
    
    for i in range(n_simulations):
        sample = poisson.rvs(mu=lambda_true, size=n)
        lambda_hat = np.mean(sample)
        tau_hat = lambda_hat + lambda_hat**2
        
        asymptotic_var = (lambda_hat * (1 + 2*lambda_hat)**2) / n
        margin = z_alpha * np.sqrt(asymptotic_var)
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
plt.savefig('task2_plot.png', dpi=300)
plt.show()
