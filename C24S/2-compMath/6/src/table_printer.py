def print_table(xs, y_euler, y_rk4, y_adams, y_exact):
    header = f"{'x':>10} {'Euler':>15} {'RK4':>15} {'Adams':>15} {'Exact':>15}"
    print(header)
    print('-' * len(header))
    for i in range(len(xs)):
        print(f"{xs[i]:>10.5f} {y_euler[i]:>15.8f} {y_rk4[i]:>15.8f} {y_adams[i]:>15.8f} {y_exact[i]:>15.8f}")