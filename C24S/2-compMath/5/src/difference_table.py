from interpolators import div_diffs

def make_table(y):
    n = len(y)
    tab = [y[:]]
    for lvl in range(1, n):
        prev = tab[lvl-1]
        curr = [prev[i+1] - prev[i] for i in range(n-lvl)]
        tab.append(curr)
    return tab

def print_table(x, y):
    tab = make_table(y)
    headers = [f"Δ^{i}" for i in range(len(tab))]
    print("| x     | " + " | ".join(headers) + " |")
    print("|" + "-------|"*(len(headers)+1))
    for i, xv in enumerate(x):
        row = [f"{xv:.4f}"] + [f"{tab[l][i]:.4f}" if i < len(tab[l]) else "" for l in range(len(tab))]
        print("| " + " | ".join(row) + " |")

def print_divided(x, y):
    tab = div_diffs(x, y)
    n = len(x)
    print("Разделенные разности:")
    for i in range(n):
        print(f"x[{i}]={x[i]:.4f}", end=": ")
        for j in range(n-i):
            print(f"{tab[j][i]:.4f}", end=" ")
        print()
