#include "utils.h"

int prim(int sideLen, const vector<int>& vertices)
{
    int n = vertices.size();
    vector<bool> relaxed(n, false);
    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> toRelax;

    int cost = 0;
    toRelax.push(make_pair(0, 0));
    while (!toRelax.empty())
    {
        int u = toRelax.top().second;
        int minW = toRelax.top().first;
        toRelax.pop();
        if (relaxed[u])
            continue;

        relaxed[u] = true;
        cost += minW;
        int ux = vertices[u] / sideLen;
        int uy = vertices[u] % sideLen;

        for (int v = 0; v < n; v++)
        {
            if (v == u || relaxed[v])
                continue;
            int vx = vertices[v] / sideLen;
            int vy = vertices[v] % sideLen;
            int w = abs(ux - vx) + abs(uy - vy);
            toRelax.push(make_pair(w, v));
        }
    }

    return cost;
}
