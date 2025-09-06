import random
from collections import deque
import time

def generate_maze(N=30, output_file="maze.txt"):
    random.seed(time.time())  # Đảm bảo mỗi lần chạy mê cung khác nhau
    H = N
    W = N

    dx = [-2, 0, 2, 0]
    dy = [0, 2, 0, -2]
    fx = [0, 0, -1, 1]
    fy = [1, -1, 0, 0]

    Sx, Sy = 1, 1
    Tx, Ty = H - 2, W - 2

    def in_bounds(x, y):
        return 0 <= x < H and 0 <= y < W

    def build_maze():
        nonlocal maze, visited
        maze = [['#' for _ in range(W)] for _ in range(H)]
        visited = [[False for _ in range(W)] for _ in range(H)]

        sx = random.randrange(1, H, 2)
        sy = random.randrange(1, W, 2)
        maze[sx][sy] = '.'
        visited[sx][sy] = True

        walls = []
        for d in range(4):
            nx, ny = sx + dx[d], sy + dy[d]
            if in_bounds(nx, ny):
                walls.append((nx, ny, d))

        while walls:
            idx = random.randint(0, len(walls) - 1)
            x, y, d = walls[idx]
            walls[idx], walls[-1] = walls[-1], walls[idx]
            walls.pop()

            px, py = x + dx[d ^ 2], y + dy[d ^ 2]
            if not in_bounds(px, py) or visited[x][y] or not visited[px][py]:
                continue

            visited[x][y] = True
            maze[x][y] = '.'
            maze[(x + px) // 2][(y + py) // 2] = '.'

            for nd in range(4):
                nx, ny = x + dx[nd], y + dy[nd]
                if in_bounds(nx, ny) and not visited[nx][ny]:
                    walls.append((nx, ny, nd))

        # Đặt điểm bắt đầu và kết thúc
        maze[Sx][Sy] = 'S'
        maze[Tx][Ty] = 'T'

    def has_valid_path():
        check = [[False for _ in range(W)] for _ in range(H)]
        q = deque([(Sx, Sy)])
        check[Sx][Sy] = True

        while q:
            x, y = q.popleft()
            if (x, y) == (Tx, Ty):
                return True
            for i in range(4):
                nx, ny = x + fx[i], y + fy[i]
                if in_bounds(nx, ny) and not check[nx][ny] and maze[nx][ny] != '#':
                    check[nx][ny] = True
                    q.append((nx, ny))
        return False

    while True:
        maze = []
        visited = []
        build_maze()
        if has_valid_path():
            break

    with open(output_file, "w") as f:
        for row in maze:
            f.write("".join(row) + "\n")

if __name__ == "__main__":
    generate_maze()  