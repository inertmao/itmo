
# Лабораторная работа №2 по вычислительной математике
**Тема:** Решение скалярных нелинейных уравнений и систем нелинейных уравнений

<img alt="Я воин Дракона!" src="https://github.com/inertmao/itmo/blob/main/.docx/itmo2.gif">

---
## 📂 Структура репозитория

<pre>
Lab-2/
├── <a href="https://github.com/inertmao/itmo/tree/main/C24S/2-compMath/Lab-2/PyCode">PyCode/</a>               Основные Python-скрипты
├── <a href="https://github.com/inertmao/itmo/tree/main/C24S/2-compMath/Lab-2/graph">graph/</a>                Сгенерированные графики
├── <a href="https://github.com/inertmao/itmo/tree/main/C24S/2-compMath/Lab-2/report">report/</a>              Скомпилированный PDF-отчёт
│   └── <a href="https://github.com/inertmao/itmo/tree/main/C24S/2-compMath/Lab-2/report/TexReport">TexReport/</a>   Исходники отчёта на LaTeX
└── <a href="https://github.com/inertmao/itmo/tree/main/C24S/2-compMath/Lab-2/solutions">solutions/</a>          Примеры работы и готовые решения
</pre>


---

## 🚀 Быстрый старт

1. **Клонирование репозитория**
   git clone [https://github.com/inertmao/itmo.git](https://github.com/inertmao/itmo.git)
   cd itmo/C24S/2-compMath/Lab-2

2. **Установка зависимостей**
   pip install numpy scipy matplotlib

3. **Запуск скрипта**
   cd PyCode
   python3 main.py

   * main.py: меню выбора типа задачи, метода (бисекция, Ньютона, итерации) и способа ввода (консоль/файл)

---

## 📂 Описание каталогов

### PyCode/

* main.py — точка входа, выбор уравнения/системы, метода, ввода
* non\_linear\_equation.py — методы решения одного уравнения
* non\_linear\_system.py — решение систем двух уравнений
* data\_input.py — функции ввода и парсинга данных

### graph/

Графики результатов:

* Функция + корень
* Погрешность по итерациям
* Сравнение методов

### report/

* Lab2\_Report.pdf — готовый отчёт
* TexReport/ — исходники LaTeX: report.tex, sections/, images/, Makefile или инструкции

Сборка отчёта:
cd report/TexReport
pdflatex report.tex
bibtex report
pdflatex report.tex
pdflatex report.tex
mv report.pdf ../Lab2\_Report.pdf

### solutions/

Примеры запуска: скрипты-демонстраторы, файлы входных данных, ожидаемые результаты

---

## ✍️ Содержание отчёта

1. Введение — постановка задачи
2. Теория — бисекция, Ньютона, простая итерация
3. Реализация — структура кода, описание модулей
4. Результаты — таблицы, графики, эмпирическое покрытие
5. Заключение — сравнение методов, выводы

---

## 🙋‍ Автор и контакты

Faiziev Faridun (inertmao)
ИТМО, ФПМИ
GitHub: [https://github.com/inertmao](https://github.com/inertmao)
Email: inertmao@gmail.com

---

## 📜 Лицензия

MIT License — подробности в файле LICENSE.
