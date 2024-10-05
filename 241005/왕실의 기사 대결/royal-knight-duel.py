import sys
from collections import deque
input = sys.stdin.readline

L, N, Q = map(int, input().split())

chess = [list(map(int, input().split())) for _ in range(L)]
knight_list = []
alive_list = []

dx = [0, 1, 0, -1]
dy = [-1, 0, 1, 0]


class Knight:
    def __init__(self, info):
        self.y = info[0] - 1
        self.x = info[1] - 1
        self.h = info[2]
        self.w = info[3]
        self.k = info[4]
        self.cur = info[4]

for i in range(N):
    knight_info = list(map(int, input().split()))
    knight = Knight(knight_info)
    knight_list.append(knight)
    alive_list.append(i+1)

def move_knight(start, direction):
    queue = deque() #이동 대상 기사
    queue.append(start)
    move_list = [] #이동 예정 기사
    move_list.append(start)
    damage = [0 for _ in range(N+1)]
    while queue:
        knight_idx = queue.popleft()
        knight = knight_list[knight_idx-1]
        #이동 후 벽 체크 벽 겹칠 시 return
        nx = knight.x+dx[direction]
        ny = knight.y+dy[direction]
        nw = knight.w
        nh = knight.h
        for i in range(nx, nx+nw):
            for j in range(ny, ny+nh):
                if (i < 0 or L <= i or j < 0 or L <= j):
                    #외벽
                    return
                if (chess[j][i] == 2):
                    #내벽
                    return
                if (chess[j][i] == 1):
                    damage[knight_idx] += 1
        #겹치는 기사 체크, 해당 기사 queue append
        for k in range(len(alive_list)):
            if alive_list[k] in move_list:
                continue
            compare_knight = knight_list[alive_list[k]-1]
            cx = compare_knight.x
            cy = compare_knight.y
            cw = compare_knight.w
            ch = compare_knight.h
            if nx <= cx+cw-1 and nx+nw-1 >= cx and  ny <= cy+ch-1 and ny+nh-1 >= cy:
                queue.append(alive_list[k])
                move_list.append(alive_list[k])
    for knight_idx in move_list:
        knight_list[knight_idx-1].x = knight_list[knight_idx-1].x+dx[direction]
        knight_list[knight_idx-1].y = knight_list[knight_idx-1].y+dy[direction]
        if (start != knight_idx):
            knight_list[knight_idx-1].cur = knight_list[knight_idx-1].cur - damage[knight_idx]
            if(knight_list[knight_idx-1].cur <= 0):
                alive_list.remove(knight_idx)
answer = 0

for _ in range(Q):
    I, J = map(int, input().split())
    #명령 수행
    move_knight(I, J)

for item in alive_list:
    answer += knight_list[item-1].k - knight_list[item-1].cur


print(answer)