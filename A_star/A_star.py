import numpy as np
import operator

# 城市编号0~19对应城市名
city = ["Arad", "Bucharest", "Craiova", "Dobreta", "Eforie", "Fagaras", "Giuriu", "Hirsova", "Iasi",
        "Lugoj", "Mehadia", "Neamt", "Oradea", "Pitesti", "Rimnicu Vilcea", "Sibiu", "Timisoara", "Urziceni", "Vaslui",
        "Zerind"]

# 城市编号0~19对应到Bucharest的直线距离(h(n))
h = [366, 0, 160, 242, 161, 178, 77, 151, 226, 244, 241, 234, 380, 98, 193, 253, 329, 80, 199, 374]

# 根据地图将每条边的cost用20*20矩阵存起来
edge = np.zeros((20, 20))
edge[0, 19] = edge[19, 0] = 75
edge[0, 15] = edge[15, 0] = 140
edge[0, 16] = edge[16, 0] = 118
edge[1, 5] = edge[5, 1] = 211
edge[1, 13] = edge[13, 1] = 101
edge[1, 6] = edge[6, 1] = 90
edge[1, 17] = edge[17, 1] = 85
edge[2, 3] = edge[3, 2] = 120
edge[2, 14] = edge[14, 2] = 146
edge[2, 13] = edge[13, 2] = 138
edge[3, 10] = edge[10, 3] = 75
edge[4, 7] = edge[7, 4] = 86
edge[5, 15] = edge[15, 5] = 99
edge[7, 17] = edge[17, 7] = 98
edge[8, 11] = edge[11, 8] = 226
edge[8, 18] = edge[18, 8] = 92
edge[9, 10] = edge[10, 9] = 70
edge[9, 16] = edge[16, 9] = 111
edge[12, 19] = edge[19, 12] = 71
edge[12, 15] = edge[15, 12] = 151
edge[13, 14] = edge[14, 13] = 97
edge[14, 15] = edge[15, 14] = 80
edge[17, 18] = edge[18, 17] = 142

global destination


class Node:
    def __init__(this, number, parent):
        this.number = number
        this.parent = parent
        this.f = this.G() + abs(h[this.number] - h[destination])
        this.g = this.G()

    def G(this):
        if this.parent == None:
            return 0
        else:
            return this.parent.G() + edge[this.parent.number, this.number]

    def adjacentNodes(this):  # 获取相邻节点
        children = []
        for x in range(20):
            if edge[this.number, x] > 0:  # 大于0说明有cost,即此路是通的
                children.append(Node(x, this))
        return children


def A_Star(Start, Destination):
    openList = []
    closeList = []
    openList.append(Start)
    while len(openList) > 0:
        openList.sort(key=operator.attrgetter('f'), reverse=True)  # 按f从大到小排序
        best = openList.pop()  # 取出f(n)最小的
        closeList.append(best)
        if (best.number == Destination.number):  # 结束条件
            Destination.parent = best.parent
            break
        else:
            nextNodes = best.adjacentNodes()
            for i in nextNodes:
                if i in openList:  # 如果i在openList中
                    if best.f < i.parent.f:
                        i.parent = best
                elif i in closeList:  # 如果i在closeList中则查找下一个点
                    continue
                else:  # 如果i既不在openList也不在closeList，则加入openList
                    openList.append(i)
    record = Destination
    recordList = []
    while record.parent != None:
        recordList.append(record.number)
        record = record.parent
    recordList.append(Start.number)
    path = list(reversed(recordList))  # 逆序
    cost = 0
    # 输出结果
    print("Thr path is:", end=" ")
    for i in range(len(path) - 1):
        print(city[path[i]], end='->')
        cost += edge[path[i], path[i + 1]]  # 计算cost
    print(city[Destination.number])
    print("The total cost is", int(cost), ".")


# 用户交互
for i in range(20):
    print(i, ":", city[i])
print("Please input the number of the city!")
start = int(input("start:"))
destination = int(input("destination:"))
Start = Node(start, None)
Destination = Node(destination, None)
A_Star(Start, Destination)
