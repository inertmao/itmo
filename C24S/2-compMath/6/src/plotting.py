import matplotlib.pyplot as plt

def plot_all_solutions(xs, y_exact, y_euler, y_rk4, y_adams):
    plt.figure()
    plt.plot(xs, y_exact, label='Exact', color='black')
    plt.plot(xs, y_euler, label='Euler', linestyle='--')
    plt.plot(xs, y_rk4, label='RK4', linestyle='-.')
    plt.plot(xs, y_adams, label='Adams', linestyle=':')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title("Сравнение точного и приближённых решений")
    plt.legend()
    plt.grid(True)
    plt.show()