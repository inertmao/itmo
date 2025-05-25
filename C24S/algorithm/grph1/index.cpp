#include <algorithm>
#include <iostream>

using namespace std;

const int INF = 1e9;
const int MAX_ROWS = 1000;
const int MAX_COLS = 1000;

struct Point {
  int row;
  int col;
};

struct ha {
  Point a[MAX_ROWS * MAX_COLS * 4];
  int b[MAX_ROWS * MAX_COLS * 4];
  int sz;
  ha() : sz(0) {
  }
  void insert(Point p, int cost) {
    a[sz] = p;
    b[sz] = cost;
    int pos = sz++;
    while (pos > 0 && b[pos] < b[(pos - 1) / 2]) {
      swap(a[pos], a[(pos - 1) / 2]);
      swap(b[pos], b[(pos - 1) / 2]);
      pos = (pos - 1) / 2;
    }
  }
  Point getMin() {
    return a[0];
  }
  int getMinCost() {
    return b[0];
  }
  void removeMin() {
    sz--;
    a[0] = a[sz];
    b[0] = b[sz];
    int pos = 0;
    while (true) {
      int l = 2 * pos + 1;
      int r = 2 * pos + 2;
      int s = pos;
      if (l < sz && b[l] < b[s])
        s = l;
      if (r < sz && b[r] < b[s])
        s = r;
      if (s == pos)
        break;
      swap(a[pos], a[s]);
      swap(b[pos], b[s]);
      pos = s;
    }
  }
  bool empty() {
    return sz == 0;
  }
};

int rows, cols;
static char grid[MAX_ROWS][MAX_COLS];
static int distArr[MAX_ROWS * MAX_COLS];
static char parentMove[MAX_ROWS * MAX_COLS];

int dr[4] = {-1, 0, 1, 0};
int dc[4] = {0, 1, 0, -1};
char dirChar[4] = {'N', 'E', 'S', 'W'};

inline int idx(int r, int c) {
  return r * cols + c;
}

void reversePath(char* path, int len) {
  for (int i = 0, j = len - 1; i < j; ++i, --j)
    swap(path[i], path[j]);
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  cin >> rows >> cols;
  int sr, sc, tr, tc;
  cin >> sr >> sc >> tr >> tc;
  --sr;
  --sc;
  --tr;
  --tc;

  for (int r = 0; r < rows; ++r)
    for (int c = 0; c < cols; ++c)
      cin >> grid[r][c];

  int total = rows * cols;
  for (int i = 0; i < total; ++i) {
    distArr[i] = INF;
    parentMove[i] = 0;
  }

  ha pq;
  int start = idx(sr, sc);
  int target = idx(tr, tc);
  distArr[start] = 0;
  pq.insert({sr, sc}, 0);

  while (!pq.empty()) {
    int cost = pq.getMinCost();
    Point p = pq.getMin();
    pq.removeMin();
    int u = idx(p.row, p.col);
    if (cost != distArr[u])
      continue;
    if (u == target)
      break;
    for (int i = 0; i < 4; ++i) {
      int nr = p.row + dr[i];
      int nc = p.col + dc[i];
      if (nr < 0 || nr >= rows || nc < 0 || nc >= cols)
        continue;
      char ch = grid[nr][nc];
      if (ch == '#')
        continue;
      int w = (ch == '.' ? 1 : 2);
      int v = idx(nr, nc);
      if (cost + w < distArr[v]) {
        distArr[v] = cost + w;
        parentMove[v] = dirChar[i];
        pq.insert({nr, nc}, distArr[v]);
      }
    }
  }

  if (distArr[target] == INF) {
    cout << -1;
    return 0;
  }

  cout << distArr[target] << '\n';
  char path[MAX_ROWS * MAX_COLS];
  int len = 0;
  int cur = target;
  while (cur != start) {
    char mv = parentMove[cur];
    path[len++] = mv;
    int r = cur / cols;
    int c = cur % cols;
    if (mv == 'N')
      ++r;
    else if (mv == 'S')
      --r;
    else if (mv == 'E')
      --c;
    else if (mv == 'W')
      ++c;
    cur = idx(r, c);
  }
  reversePath(path, len);
  for (int i = 0; i < len; ++i)
    cout << path[i];
  cout << '\n';
  return 0;
}
