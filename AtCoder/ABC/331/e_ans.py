N, M, L = map(int, input().split())
a = list(map(int, input().split()))
b = list(map(int, input().split()))
g = [set() for _ in range(N)]
for _ in range(L):
    c, d = map(lambda x: int(x) - 1, input().split())
    g[c].add(d)
s = sorted([(p, j) for j, p in enumerate(b)], reverse=True)
ans = 0
for i in range(N):
    for p, j in s:
        if j not in g[i]:
            ans = max(ans, a[i] + p)
            break
print(ans)