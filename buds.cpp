#include <bits/stdc++.h>
using namespace std;

void dfs(int u, int parent, vector<vector<int> > &G, vector<bool> &colors){
    bool is_blue = true;
    for(int v : G[u]){
        if(v != parent){
            dfs(v, u, G, colors);
            if(colors[v]) is_blue = false;
        }
    }
    colors[u] = is_blue;
}

void solve(){
    int n;
    cin >> n;
    vector<vector<int> > G(n);
    for(int i = 0; i < n-1; ++i){
        int u, v;
        cin >> u >> v;
        --u, --v;
        G[u].push_back(v), G[v].push_back(u);
    }

    vector<bool> colors(n);
    dfs(0, -1, G, colors);

    int ans = 0;
    for(int u = 1; u < n; ++u){
        if(colors[u]) ans++;
        else ans--;
    }
    if(colors[0]){
        ans++;
    }
    cout << ans << endl;
}

int main(){
    int t;
    cin >> t;
    while(t--) solve();
}
