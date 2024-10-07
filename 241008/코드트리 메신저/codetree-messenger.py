from collections import deque

N, Q = map(int, input().split())

chat_list = []

class Chat:
    def __init__(self, parent, auth):
        self.parent = parent
        self.child = []
        self.alarm = True
        self.auth = auth
    def __str__ (self):
        return '({}, {}, {}, {})'.format(self.parent, self.child, self.alarm, self.auth)

def init(init_list):
    for i in range(N):
        chat = Chat(init_list[i]-1, init_list[i+N])
        chat_list.append(chat)
    for i in range(N):
        parent_idx = chat_list[i].parent
        if (parent_idx > -1):
            chat_list[parent_idx].child.append(i)
    
def toggleAlarm(idx):
    if (chat_list[idx].alarm):
        chat_list[idx].alarm = False
    else:
        chat_list[idx].alarm = True
    return

def changeAuth(idx, power):
    chat_list[idx].auth = power
    return

def changeParent(idx1, idx2):
    idx1_parent = chat_list[idx1].parent
    idx2_parent = chat_list[idx2].parent

    chat_list[idx1].parent = idx2_parent
    chat_list[idx2].parent = idx1_parent

    chat_list[idx1_parent].child.remove(idx1)
    chat_list[idx1_parent].child.append(idx2)
    chat_list[idx2_parent].child.remove(idx2)
    chat_list[idx2_parent].child.append(idx1)

    return

def countChat(idx):
    cnt = 0
    que = deque()
    for c in chat_list[idx].child:
        que.appendleft([c, 1])

    while que:
        child_idx, child_depth = que.pop()
        child_chat = chat_list[child_idx]
        if (child_chat.alarm == False):
            return cnt
        if (child_depth <= child_chat.auth):
            cnt += 1
        for c in child_chat.child:
            que.appendleft([c, child_depth+1])

    return cnt

for _ in range(Q):
    cmd = list(map(int, input().split()))
    if (cmd[0] == 100):
        init(cmd[1:])
    elif (cmd[0] == 200):
        toggleAlarm(cmd[1]-1)
    elif (cmd[0] == 300):
        changeAuth(cmd[1]-1, cmd[2])
    elif (cmd[0] == 400):
        changeParent(cmd[1]-1, cmd[2]-1)
    elif (cmd[0] == 500):
        print(countChat(cmd[1]-1))