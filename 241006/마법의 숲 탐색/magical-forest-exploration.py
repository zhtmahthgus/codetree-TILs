from collections import deque
import copy

R, C, K = map(int, input().split())

forest = [[0]*R for _ in range(C)]
golem_dir = [0 for _ in range(K)]

def check_move_s(idx, x, y):
    if (y+2 >= R):
        return False
    if (y == -2):
        if (forest[x][y+2] == 0):
            return True
    elif (forest[x-1][y+1] == 0 and forest[x+1][y+1] == 0 and forest[x][y+2] == 0):
        return True
    
    return False

def check_move_w(idx, x, y):
    if (x-2 < 0 or y+2>=R):
        return False
    if (y == -2):
        if (forest[x-1][y+2] == 0):
            return True
    elif (y == -1):
        if (forest[x-1][y+1] == 0 and forest[x-2][y+1] == 0 and forest[x-1][y+2] == 0):
            return True
    elif (y == 0):
        if (forest[x-2][y] == 0 and forest[x-1][y+1] == 0 and forest[x-2][y+1] == 0 and forest[x-1][y+2] == 0):
            return True
    else:
        if (forest[x-1][y-1] == 0 and forest[x-2][y] == 0 and forest[x-1][y+1] == 0
        and forest[x-2][y+1] == 0 and forest[x-1][y+2] == 0):
            return True

    return False

def check_move_e(idx, x, y):
    if (x+2 >= C and y+2<R):
        return False
    if (y == -2):
        if (forest[x+1][y+2] == 0):
            return True
    elif (y == -1):
        if (forest[x+1][y+1] == 0 and forest[x+2][y+1] == 0 and forest[x+1][y+2] == 0):
            return True
    elif (y == 0):
        if (forest[x+2][y] == 0 and forest[x+1][y+1] == 0 and forest[x+2][y+1] == 0 and forest[x+1][y+2] == 0):
            return True
    else:
        if (forest[x+1][y-1] == 0 and forest[x+2][y] == 0 and forest[x+1][y+1] == 0
        and forest[x+2][y+1] == 0 and forest[x+1][y+2] == 0):
            return True

    return False


def check_move(idx, start_x, start_y):
    if start_y+2 == R:
        return [start_x, start_y]
    if check_move_s(idx, start_x, start_y):
        x, y = check_move(idx, start_x, start_y+1)
    elif check_move_w(idx, start_x, start_y):
        if (golem_dir[idx] == 0):
            golem_dir[idx] = 3
        else:
            golem_dir[idx] -= 1
        x, y = check_move(idx, start_x-1, start_y+1)
    elif check_move_e(idx, start_x, start_y):
        if (golem_dir[idx] == 3):
            golem_dir[idx] = 0
        else:
            golem_dir[idx] += 1
        x, y = check_move(idx, start_x+1, start_y+1)
    else:
        x, y = [start_x, start_y]
    return [x, y]
    

def get_row(idx, x, y):
    #dfs
    que = deque()
    visited =  [[0]*R for _ in range(C)]
    result = -1

    dx = [0, 1, 0, -1]
    dy = [-1, 0, 1, 0]

    que.appendleft([x, y, forest[x][y]])

    
    while que:
        px, py, pv = que.pop()
        visited[px][py] = 1

        if result < py :
            result = py
        for i in range(4):
            nx = px + dx[i]
            ny = py + dy[i]
            if (0 <= nx < C and 0 <= ny < R and visited[nx][ny] != 1 and forest[nx][ny] != 0):
                if (pv > 0):
                    if (forest[nx][ny] == pv or forest[nx][ny] == pv * -1):
                        visited[nx][ny] = 1
                        que.appendleft([nx, ny, forest[nx][ny]])
                if (pv < 0):
                    if (forest[nx][ny] != 0):
                        visited[nx][ny] = 1
                        que.appendleft([nx, ny, forest[nx][ny]])
    
    return result

            
            



def move_g(idx, start_x):
    global forest
    x, y = check_move(idx, start_x-1, -2)
    if (y < 1) :
        forest = [[0]*R for _ in range(C)]
        return 0
    else:
        forest[x][y] = idx+1
        forest[x][y-1] = idx+1
        forest[x+1][y] = idx+1
        forest[x][y+1] = idx+1
        forest[x-1][y] = idx+1
        if golem_dir[idx] == 0:
            forest[x][y-1] *= -1
        elif golem_dir[idx] == 1:
            forest[x+1][y] *= -1
        elif golem_dir[idx] == 2:
            forest[x][y+1] *= -1
        elif golem_dir[idx] == 3:
            forest[x-1][y] *= -1
        return get_row(idx, x, y) + 1

answer = 0

for i in range(K):
    Ci, Di = map(int, input().split())
    golem_dir[i] = Di
    answer += move_g(i, Ci)

print(answer)