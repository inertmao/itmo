import numpy as np
import matplotlib.pyplot as plt

def plot_function(f, a, b, root=None):
    x_vals = np.linspace(a, b, 400)
    y_vals = np.array([f(x) for x in x_vals])
    
    plt.figure()
    plt.plot(x_vals, y_vals, label="y")
    plt.axhline(0, color='black', linewidth=0.5)
    
    if root is not None:
        plt.scatter(root, f(root), color='green', zorder=3, label="Корень")
    
    plt.title("График функции")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_system(F, interval_x, interval_y, root=None, system_label="Система"):
    x_vals = np.linspace(interval_x[0], interval_x[1], 400)
    y_vals = np.linspace(interval_y[0], interval_y[1], 400)
    X, Y = np.meshgrid(x_vals, y_vals)
    
  
    Z1 = F(np.array([X, Y]))[0]
    Z2 = F(np.array([X, Y]))[1]
    
    plt.figure()
    plt.contour(X, Y, Z1, levels=[0], colors='blue')
    plt.contour(X, Y, Z2, levels=[0], colors='red')
    
    if root is not None:
        plt.scatter(root[0], root[1], color='green', marker='o', s=50, zorder=3, label="Решение")

    plt.title(f"График системы: {system_label}")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.grid(True)
    plt.show()
