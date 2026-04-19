def minesweeper(some):
    m=len(some)
    for i in range(m):
        for j in range(m):
            if some[i][j] == "#":
                continue
            count = 0
            for di in [-1,0,1]:
                for dj in [-1,0,1]:
                    if di == 0 and dj == 0:
                        continue
                    ni = i + di
                    nj = j + dj
                    if 0 <= ni < m and 0 <= nj < m and some[ni][nj] == "#":
                        count += 1
            some[i][j] = str(count)
    return some
matrix = []
n = int(input())
for _ in range(n):
    row = input().split()
    matrix.append(row)

transformed = minesweeper(matrix)
for row in transformed:
    print("   ".join(row))