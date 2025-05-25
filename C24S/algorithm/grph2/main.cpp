#include <iostream>
using namespace std;

void mysort(int* a, int n) {
  for (int i = 0; i < n; i++) {
    for (int j = i + 1; j < n; j++) {
      if (a[j] < a[i]) {
        int t = a[i];
        a[i] = a[j];
        a[j] = t;
      }
    }
  }
}

int main() {
  int a;
  cin >> a;
  int b[2005];
  for (int i = 0; i < a; i++) {
    cin >> b[i];
    b[i]--;
  }
  int c[2005];
  for (int i = 0; i < a; i++)
    c[i] = 0;
  int d = 0;
  for (int i = 0; i < a; i++) {
    if (c[i] != 0)
      continue;
    int e = i;
    int f[2005];
    int g = 0;
    while (c[e] == 0) {
      c[e] = 1;
      f[g++] = e;
      e = b[e];
    }
    if (c[e] == 1)
      d++;
    for (int j = 0; j < g; j++) {
      c[f[j]] = 2;
    }
  }
  cout << d << "\n";
  return 0;
}