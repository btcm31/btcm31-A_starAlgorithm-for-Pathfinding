from queue import PriorityQueue
import math
import pygame


def heuristic(curr,end):
    y1,x1 = curr
    y2,x2 = end
    return  math.sqrt((x1-x2)**2+(y1-y2)**2)
def reconstruct_path(came_from,endPoint):#min path from start point to endpoint
    path = []
    curr = endPoint
    while curr in came_from:
        curr = came_from[curr]
        if curr!= None:
            path.append(curr)
    return path
def A_starAlgorithm(start,end,grid,draw,win):
    path = []
    frontier = PriorityQueue()
    frontier.put((0,start))
    came_from = dict()
    came_from[start] = None
    g_func = {spot: float("inf") for row in grid for spot in row}
    g_func[start] = 0
    f_func = {spot: float("inf") for row in grid for spot in row}
    f_func[start] = 0
    visited = []
    openList = [start]
    while not frontier.empty():
        curr = frontier.get()[1]
        visited.append(curr)
        if end in visited:
            path = reconstruct_path(came_from,end)
            path.append(end)
            break
        for neighbor in curr.neighbors:
            if neighbor not in visited:
                f_temp = g_func[curr] + 1 + heuristic(neighbor.get_pos(),end.get_pos())
                if neighbor not in openList or g_func[neighbor] > g_func[curr] + 1:
                    openList.append(neighbor)
                    came_from[neighbor] = curr
                    g_func[neighbor] = g_func[curr] + 1
                    f_func[neighbor] = f_temp
                    frontier.put((f_temp,neighbor))
                    if neighbor!=start and neighbor!=end and not neighbor.is_barrier():
                        neighbor.make_neighbor()
        draw()
    return path