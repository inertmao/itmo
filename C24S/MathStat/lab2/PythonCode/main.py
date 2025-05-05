#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main.py — расчёт и анализ 95%-го доверительного интервала
для τ = σ1²/σ2² по Лабораторной работе №2 (MathStat).
Исправлено: корректное создание hist_n25.
"""

import numpy as np
from scipy.stats import f
import pandas as pd
import matplotlib.pyplot as plt

# Фиксируем семя для воспроизводимости
np.random.seed(42)

# Истинные параметры
sigma1_sq = 2.0
sigma2_sq = 1.0
true_tau = sigma1_sq / sigma2_sq

def ci_ratio(x1: np.ndarray, x2: np.ndarray, alpha: float = 0.05):
    """Возвращает доверительный интервал [lower, upper] для τ по данным x1, x2."""
    s1 = np.var(x1, ddof=1)
    s2 = np.var(x2, ddof=1)
    df = len(x1) - 1
    F_low = f.ppf(alpha/2, df, df)
    F_up  = f.ppf(1 - alpha/2, df, df)
    ratio = s1 / s2
    return ratio / F_up, ratio / F_low

def simulate_stats(n: int, reps: int = 1000, alpha: float = 0.05):
    """
    Симуляция: генерирует reps пар выборок размера n,
    возвращает coverage, mean_width, std_width.
    """
    widths = []
    hits = 0
    for _ in range(reps):
        x1 = np.random.normal(0, np.sqrt(sigma1_sq), n)
        x2 = np.random.normal(0, np.sqrt(sigma2_sq), n)
        lo, hi = ci_ratio(x1, x2, alpha)
        widths.append(hi - lo)
        if lo <= true_tau <= hi:
            hits += 1
    return hits / reps, np.mean(widths), np.std(widths)

def main():
    # 1) Сравнение для n=25 и n=10000
    summary = []
    for n in [25, 10000]:
        cov, mean_w, std_w = simulate_stats(n)
        summary.append({'n': n, 'coverage': cov,
                        'mean_width': mean_w, 'std_width': std_w})
    df = pd.DataFrame(summary)
    print(df.to_string(index=False))

    # 2) Гистограмма ширин для n = 25
    widths25 = []
    for _ in range(1000):
        x1 = np.random.normal(0, np.sqrt(sigma1_sq), 25)
        x2 = np.random.normal(0, np.sqrt(sigma2_sq), 25)
        lo, hi = ci_ratio(x1, x2)
        widths25.append(hi - lo)

    plt.figure(figsize=(6,4))
    plt.hist(widths25, bins=20, edgecolor='black')
    plt.title('Гистограмма ширин доверительного интервала (n=25)')
    plt.xlabel('Ширина интервала')
    plt.ylabel('Частота')
    plt.tight_layout()
    plt.savefig('hist_n25.png')
    print("Гистограмма сохранена как hist_n25.png")

    # 3) Зависимость средней ширины от n
    n_values = [25, 50, 100, 200, 500, 1000, 2000, 5000, 10000]
    mean_widths = []
    for n in n_values:
        _, mw, _ = simulate_stats(n)
        mean_widths.append(mw)

    plt.figure(figsize=(6,4))
    plt.plot(n_values, mean_widths, marker='o', linestyle='-')
    plt.xscale('log')
    plt.yscale('log')
    plt.title('Средняя ширина доверительного интервала vs объём выборки')
    plt.xlabel('Объём выборки n (лог-шкала)')
    plt.ylabel('Средняя ширина (лог-шкала)')
    plt.grid(True, which='both', ls='--', lw=0.5)
    plt.tight_layout()
    plt.savefig('width_vs_n.png')
    print("График зависимости средней ширины сохранён как width_vs_n.png")

if __name__ == '__main__':
    main()

