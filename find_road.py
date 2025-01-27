from config import level_hitboxes
from collections import deque

def find_road(start_point: tuple, end_point: tuple):
    graph = level_hitboxes.copy()
    x_NPS, y_NPS = start_point
    e_x, e_y = end_point
    graph[e_y][e_x] = "E"
    graph[y_NPS][x_NPS] = "N"
    graph = ["".join(i) for i in graph]


    road = bfs(graph, start_point[::-1], end_point[::-1])
    return road
                


def is_valid_move(r, c, graph, visited):
    return (0 <= r < len(graph) and 
            0 <= c < len(graph[0]) and 
            graph[r + 1][c] != '1' and 
            graph[r + 2][c] != "1" and
            (r, c) not in visited)

def bfs(graph, start, end):
    queue = deque([start])
    visited = set()
    visited.add(start)
    parent = {start: None}

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)] 

    while queue:
        current = queue.popleft()

        if current == end:
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            return path[::-1]  

        for direction in directions:
            next_r, next_c = current[0] + direction[0], current[1] + direction[1]
            if is_valid_move(next_r, next_c, graph, visited):
                visited.add((next_r, next_c))
                parent[(next_r, next_c)] = current
                queue.append((next_r, next_c))

    return None 


    
print(57 * 32)
