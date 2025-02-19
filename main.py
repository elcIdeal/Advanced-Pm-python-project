import pandas as pd
import heapq
import math
from collections import deque

# === 1. ЗАГРУЗКА ДАННЫХ ===
def load_data(filename):
    df = pd.read_csv(filename)
    df.columns = df.columns.str.strip()
    graph = {}

    for _, row in df.iterrows():
        start, end, distance = row['Order'], row['Destination'], row['Distance']
        if start not in graph:
            graph[start] = []
        if end not in graph:
            graph[end] = []
        graph[start].append((end, distance))
        graph[end].append((start, distance))  # Неориентированный граф

    return graph
"""
Blagodarnyy, Budonnovsk, 70
Budonnovsk, Zelenokumsk, 60

graph = {
    'Blagodarnyy': [('Budonnovsk', 70)],
    'Budonnovsk': [('Blagodarnyy', 70), ('Zelenokumsk', 60)],
    'Zelenokumsk': [('Budonnovsk', 60)]
}
This means:

Blagodarnyy is connected to Budonnovsk (70 km).
Budonnovsk is connected to Blagodarnyy and Zelenokumsk.
Zelenokumsk is connected only to Budonnovsk.
"""
# === 2. НЕИНФОРМИРОВАННЫЙ ПОИСК (BFS и DFS) ===

def bfs(start, goal, graph):
    queue = deque([(start, [start])])
    visited = set()

    while queue:
        node, path = queue.popleft()
        if node in visited:
            continue
        visited.add(node)
        if node == goal:
            return path
        for neighbor, _ in graph[node]:
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))
    return None

def dfs(start, goal, graph):
    stack = [(start, [start])]
    visited = set()

    while stack:
        node, path = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        if node == goal:
            return path
        for neighbor, _ in graph[node]:
            if neighbor not in visited:
                stack.append((neighbor, path + [neighbor]))
    return None

# === 3. ИНФОРМИРОВАННЫЙ ПОИСК (A*) ===

def heuristic(city, goal, city_coords):
    if city in city_coords and goal in city_coords:
        x1, y1 = city_coords[city]
        x2, y2 = city_coords[goal]
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)  # Евклидово расстояние
    return 0  # Если координаты неизвестны, эвристика = 0

def a_star(start, goal, graph, city_coords):
    open_list = [(0, start, [start])]
    heapq.heapify(open_list)
    g_scores = {start: 0}

    while open_list:
        cost, node, path = heapq.heappop(open_list)
        if node == goal:
            return path
        for neighbor, dist in graph[node]:
            new_cost = g_scores[node] + dist
            if neighbor not in g_scores or new_cost < g_scores[neighbor]:
                g_scores[neighbor] = new_cost
                f_score = new_cost + heuristic(neighbor, goal, city_coords)
                heapq.heappush(open_list, (f_score, neighbor, path + [neighbor]))
    return None

# === 4. АДВЕРСАРИАЛЬНЫЙ ПОИСК (МИНИМАКС / ALPHA-BETA) ===

def minimax(node, depth, maximizing, graph, alpha, beta, goal):
    if depth == 0 or node == goal:
        return 0
    if maximizing:
        max_eval = -float('inf')
        for neighbor, _ in graph[node]:
            eval = minimax(neighbor, depth - 1, False, graph, alpha, beta, goal)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for neighbor, _ in graph[node]:
            eval = minimax(neighbor, depth - 1, True, graph, alpha, beta, goal)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def alpha_beta_pruning(node, depth, maximizing, graph, alpha, beta, goal):
    return minimax(node, depth, maximizing, graph, alpha, beta, goal)

# === 5. ВЫПОЛНЕНИЕ ПРОГРАММЫ ===
graph = load_data('cities.csv')
city_coords = {
    "Blagodarnyy": (45.1, 43.4),
    "Svetlograd": (45.3, 42.9),
}

start_city, goal_city = 'Blagodarnyy', 'Svetlograd'

print("BFS Path:", bfs(start_city, goal_city, graph))
print("DFS Path:", dfs(start_city, goal_city, graph))
print("A* Path:", a_star(start_city, goal_city, graph, city_coords))
print("Minimax Evaluation:", minimax(start_city, 3, True, graph, -float('inf'), float('inf'), goal_city))
print("Alpha-Beta Evaluation:", alpha_beta_pruning(start_city, 3, True, graph, -float('inf'), float('inf'), goal_city))
