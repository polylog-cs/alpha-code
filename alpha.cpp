#include <bits/stdc++.h>
using namespace std;
const int N = 2e5 + 10;
vector<int> g[N];
int n, d[N], cnt[N];
// void dfs(int x, int fa) {
//       d[x] = d[fa] + 1;
//   for (int i = 0; i < g[x].size(); i++) {
//         int v = g[x][i];
//     if (v == fa) continue;
//     dfs(v, x);
//   }
// }
int ans;
void getans(int x, int fa) {
  int tot = 0;
  for (int i = 0; i < g[x].size(); i++) {
    int v = g[x][i];
    if (v == fa) continue;
    getans(v, x);
    tot += cnt[v];
  }
  if (tot == 0)
    cnt[x] = 1;
  else
    ans += tot - 1;
}
int main() {
      int T;
  cin >> T;
  while (T--) {
        scanf("%d", &n);
    for (int i = 1; i <= n; i++) {
          g[i].clear();
      d[i] = cnt[i] = 0;
    }
    for (int i = 1; i <= n - 1; i++) {
          int u, v;
      scanf("%d%d", &u, &v);
      g[u].push_back(v);
      g[v].push_back(u);
    }
    //dfs(1, 0);
    ans = 0;
    // for (int i = 1; i <= n; i++) {
    //       sort(g[i].begin(), g[i].end(),
    //        [&](int x, int y) { return (d[x] > d[y]); });
    // }
    getans(1, 0);
    printf("%d\n", ans + 1);
  }
  return 0;
}