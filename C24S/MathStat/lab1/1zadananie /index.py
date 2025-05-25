import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.distributions.empirical_distribution import ECDF

# Шаг 1. Загрузка и подготовка данных
df = pd.read_csv('iris.csv')
df.rename(columns={
    'Sepal.Length': 'sepal_length',
    'Sepal.Width': 'sepal_width',
    'Petal.Length': 'petal_length',
    'Petal.Width': 'petal_width',
    'Species': 'species'
}, inplace=True)

# Шаг 2. Расчёт площадей
df['sepal_area'] = df['sepal_length'] * df['sepal_width']
df['petal_area'] = df['petal_length'] * df['petal_width']
df['total_area'] = df['sepal_area'] + df['petal_area']

# Шаг 3. Частота видов
print("📌 Количество экземпляров каждого вида:")
print(df['species'].value_counts())
print("🔼 Больше всего:", df['species'].value_counts().idxmax())
print("🔽 Меньше всего:", df['species'].value_counts().idxmin())

# Шаг 4. Статистика по всей выборке
total_stats = {
    'Среднее': df['total_area'].mean(),
    'Дисперсия': df['total_area'].var(),
    'Медиана': df['total_area'].median(),
    'Квантиль 2/5': df['total_area'].quantile(0.4)
}
print("\n📊 Общая статистика по всем видам:")
for k, v in total_stats.items():
    print(f"{k}: {v:.4f}")

# Шаг 5. Статистика по видам
group_stats = df.groupby('species')['total_area'].agg([
    'mean', 'var', 'median', lambda x: x.quantile(0.4)
])
group_stats.rename(columns={
    'mean': 'Среднее',
    'var': 'Дисперсия',
    'median': 'Медиана',
    '<lambda_0>': 'Квантиль 2/5'
}, inplace=True)
print("\n📊 Статистика по видам:")
print(group_stats)

# ========== Графики ==========

# ЭФР (общая)
ecdf = ECDF(df['total_area'])
plt.figure(figsize=(10, 5))
plt.step(ecdf.x, ecdf.y, where='post')
plt.title('ЭФР — вся выборка')
plt.xlabel('Суммарная площадь')
plt.ylabel('Доля')
plt.grid(True)
plt.savefig('ecdf_all.png')
plt.close()

# ЭФР по видам
plt.figure(figsize=(10, 5))
for species_name in df['species'].unique():
    ecdf = ECDF(df[df['species'] == species_name]['total_area'])
    plt.step(ecdf.x, ecdf.y, where='post', label=species_name)
plt.title('ЭФР по видам')
plt.xlabel('Суммарная площадь')
plt.ylabel('Доля')
plt.legend()
plt.grid(True)
plt.savefig('ecdf_by_species.png')
plt.close()

# Гистограмма (общая)
plt.figure(figsize=(10, 5))
sns.histplot(df['total_area'], bins=20, kde=True)
plt.title('Гистограмма — вся выборка')
plt.xlabel('Суммарная площадь')
plt.ylabel('Частота')
plt.grid(True)
plt.savefig('hist_all.png')
plt.close()

# Гистограмма по видам
plt.figure(figsize=(10, 5))
sns.histplot(data=df, x='total_area', hue='species', bins=20,
             element='step', stat='density', common_norm=False)
plt.title('Гистограмма по видам')
plt.xlabel('Суммарная площадь')
plt.ylabel('Плотность')
plt.grid(True)
plt.savefig('hist_by_species.png')
plt.close()

# Box-plot по видам
plt.figure(figsize=(10, 5))
sns.boxplot(data=df, x='species', y='total_area')
plt.title('Box-plot по видам')
plt.xlabel('Вид цветка')
plt.ylabel('Суммарная площадь')
plt.grid(True)
plt.savefig('boxplot_by_species.png')
plt.close()
