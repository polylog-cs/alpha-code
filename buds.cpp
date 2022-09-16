#include <bits/stdc++.h>
using namespace std;

void dfs(int u, int parent, vector<vector<int> > &G, vector<bool> &is_blue){
    int blue = true;
    for(int v : G[u]){
        if(v != parent){
            dfs(v, u, G, is_blue);
            if(is_blue[v]) blue = false;
        }
    }
    is_blue[u] = blue;
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

    vector<bool> is_blue(n);
    dfs(0, -1, G, is_blue);

    int ans = 0;
    for(int u = 0; u < n; ++u){
        if(is_blue[u]) ans++;
        else ans--;
    }
    ans += 1 - is_blue[0];
    cout << ans << endl;
}

int main(){
    int t;
    cin >> t;
    while(t--) solve();
}
