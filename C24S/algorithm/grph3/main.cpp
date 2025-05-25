#include <iostream>
using namespace std;

int aa[2005][2005];
int ab[2005], ac[2005], ad[2005];

int main() {
  int a, b;
  cin >> a >> b;
  for (int i = 1; i <= a; i++)
    ab[i] = 0;
  for (int i = 0; i < b; i++) {
    int c, d;
    cin >> c >> d;
    aa[c][0]++;
    aa[c][aa[c][0]] = d;
    aa[d][0]++;
    aa[d][aa[d][0]] = c;
  }
  for (int i = 1; i <= a; i++)
    ac[i] = -1;
  int ae[2005];
  int af = 0, ag = 0;
  for (int ah = 1; ah <= a; ah++) {
    if (ac[ah] != -1)
      continue;
    ac[ah] = 0;
    ae[ag++] = ah;
    while (af < ag) {
      int ai = ae[af++];
      for (int aj = 1; aj <= aa[ai][0]; aj++) {
        int ak = aa[ai][aj];
        if (ac[ak] == -1) {
          ac[ak] = ac[ai] ^ 1;
          ae[ag++] = ak;
        } else if (ac[ak] == ac[ai]) {
          cout << "NO\n";
          return 0;
        }
      }
    }
  }
  cout << "YES\n";
  return 0;
}