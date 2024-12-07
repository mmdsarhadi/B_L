def r_g_f_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    V = int(lines[0].split()[1])
    mabda = int(lines[1].split()[1])
    graph = []

    for line in lines[3:]:
        u, v, w = map(int, line.split())
        graph.append((u, v, w))
    return V, mabda, graph


def b_f_w_c(graph, V, mabda):
    distance = [float("Inf")] * V
    p = [-1] * V
    distance[mabda] = 0

    # Relaxation of edges V-1 times
    for _ in range(V - 1):
        for u, v, w in graph:
            if distance[u] != float("Inf") and distance[u] + w < distance[v]:
                distance[v] = distance[u] + w
                p[v] = u

    # Check for negative weight cycles
    negative_cycles = set()  # Use a set to avoid duplicates
    for u, v, w in graph:
        if distance[u] != float("Inf") and distance[u] + w < distance[v]:
            # Find one negative cycle
            visited = set()
            cycle = []
            current = v

            # Traverse back V times to ensure we are within a cycle
            for _ in range(V):
                current = p[current]

            # Follow the cycle and record nodes
            start = current
            while current not in visited:
                visited.add(current)
                cycle.append(current)
                current = p[current]

            # Reorder cycle to start from the smallest node
            if cycle:
                cycle_start_idx = cycle.index(current)
                cycle = cycle[cycle_start_idx:]  # Only keep the cycle part
                negative_cycles.add(tuple(sorted(cycle)))

    if negative_cycles:
        print("Negative cycles found:")
        for cycle in negative_cycles:
            print(" -> ".join(map(str, cycle)))
        return None

    # Print shortest paths if no negative cycle
    print("Shortest paths:")
    for i in range(V):
        if distance[i] == float("Inf"):
            print(f"Node {i}: No path")
        else:
            path = []
            current = i
            while current != -1:
                path.append(current)
                current = p[current]
            print(
                f"Node {i}: Distance = {distance[i]}, Path = {' -> '.join(map(str, path[::-1]))}")
    return distance



filename = "input.txt"
V, mabda, graph = r_g_f_file(filename)
result = b_f_w_c(graph, V, mabda)
