def read_graph_from_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        num_vertices, num_edges = map(int, lines[0].split())
        edges = []
        for line in lines[1:]:
            u, v, w = map(int, line.split())
            edges.append((u, v, w))
    return num_vertices, edges

def bellman_ford(num_vertices, edges, source):

    distances = {i: float('inf') for i in range(num_vertices)}
    distances[source] = 0
    predecessors = {i: None for i in range(num_vertices)}

    for _ in range(num_vertices - 1):
        for u, v, w in edges:
            if distances[u] + w < distances[v]:
                distances[v] = distances[u] + w
                predecessors[v] = u

    # بررسی وجود مسیر یا دور منفی
    negative_cycles = []
    for u, v, w in edges:
        if distances[u] + w < distances[v]:
            cycle = []
            visited = set()
            current = v
            # یافتن یک دور منفی
            while current not in visited:
                visited.add(current)
                current = predecessors[current]
            start = current
            cycle.append(start)
            current = predecessors[start]
            while current != start:
                cycle.append(current)
                current = predecessors[current]
            cycle.append(start)
            cycle.reverse()
            negative_cycles.append(cycle)

    return distances, negative_cycles

def print_results(distances, negative_cycles):
    if negative_cycles:
        print("مسیرها یا دورهای منفی وجود دارند:")
        for cycle in negative_cycles:
            print(" -> ".join(map(str, cycle)))
    else:
        print("کوتاه‌ترین مسیرها از رأس مبدأ:")
        for node, distance in distances.items():
            print(f"فاصله تا گره {node}: {distance}")

if __name__ == "__main__":
    # فایل گراف را بخوانید
    filename = "graph.txt"
    num_vertices, edges = read_graph_from_file(filename)

    # اجرای الگوریتم بلمن-فورد از رأس مبدأ (0)
    source = 0
    distances, negative_cycles = bellman_ford(num_vertices, edges, source)

    # چاپ نتایج
    print_results(distances, negative_cycles)