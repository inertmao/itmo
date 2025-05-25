#include <iostream>
using namespace std;

int a[1000][1000];
unsigned char b[1000];
int c[1000];

int main() {
  int n;
  cin >> n;
  int d = 0;
  for (int i = 0; i < n; i++) {
    for (int j = 0; j < n; j++) {
      cin >> a[i][j];
      if (a[i][j] > d)
        d = a[i][j];
    }
  }
  if (n <= 1) {
    cout << 0 << "\n";
    return 0;
  }

  int l = 0, r = d;
  while (l < r) {
    int m = l + (r - l) / 2;
    int ch = 0, ct = 0;
    for (int i = 0; i < n; i++)
      b[i] = 0;
    b[0] = 1;
    c[ct++] = 0;
    while (ch < ct) {
      int u = c[ch++];
      for (int v = 0; v < n; v++) {
        if (!b[v] && a[u][v] <= m) {
          b[v] = 1;
          c[ct++] = v;
        }
      }
    }
    if (ct < n) {
      l = m + 1;
      continue;
    }
    ch = 0;
    ct = 0;
    for (int i = 0; i < n; i++)
      b[i] = 0;
    b[0] = 1;
    c[ct++] = 0;
    while (ch < ct) {
      int u = c[ch++];
      for (int v = 0; v < n; v++) {
        if (!b[v] && a[v][u] <= m) {
          b[v] = 1;
          c[ct++] = v;
        }
      }
    }
    if (ct < n) {
      l = m + 1;
    } else {
      r = m;
    }
  }
  cout << l << "\n";
  return 0;
}