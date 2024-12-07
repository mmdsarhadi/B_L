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
    predecessor = [-1] * V
    distance[mabda] = 0

    for _ in range(V - 1):
        for u, v, w in graph:
            if distance[u] != float("Inf") and distance[u] + w < distance[v]:
                distance[v] = distance[u] + w
                predecessor[v] = u

    has_negative_cycle = False
    for u, v, w in graph:
        if distance[u] != float("Inf") and distance[u] + w < distance[v]:
            has_negative_cycle = True
            print(
                f"N- ({u}, {v}) with weight {w}.")

            cycle = []
            current = v
            for _ in range(V):
                current = predecessor[current]
            start = current
            while True:
                cycle.append(current)
                current = predecessor[current]
                if current == start and len(cycle) > 1:
                    break
            cycle.append(start)
            print("Cycle:", " -> ".join(map(str, cycle[::-1])))

    if has_negative_cycle:
        return None

    print("Sh :")
    for i in range(V):
        if distance[i] == float("Inf"):
            print(f"Node {i}: No path")
        else:
            path = []
            current = i
            while current != -1:
                path.append(current)
                current = predecessor[current]
            print(
                f"Node {i}: Distance = {distance[i]}, Path = {' -> '.join(map(str, path[::-1]))}")
    return distance


filename = "input.txt"
V, mabda, graph = r_g_f_file(filename)


result = b_f_w_c(graph, V, mabda)
