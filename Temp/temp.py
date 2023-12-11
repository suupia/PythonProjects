N = int(input())
d = {}
for _ in range(N):
    a, b = map(int, input().split())
    if a not in d:
        d[a] = []
    if b not in d:
        d[b] = []
    d[a].append(b)
    d[b].append(a)

ans = 1
if ans not in d:
    print(ans)
    exit()
todo = [ans]
seen = set()
seen.add(1)
while todo:
    v = todo.pop()
    ans = max(ans, v)
    for u in d[v]:
        if u not in seen:
            seen.add(u)
            todo.append(u)
print(ans)