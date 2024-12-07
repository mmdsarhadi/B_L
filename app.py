from flask import Flask, render_template, request
import networkx as nx
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            V = int(request.form["vertices"])
            E = int(request.form["edges"])
            return render_template("index.html", vertices=V, edges=E, graph_input=True)
        except ValueError:
            return "Invalid input. Please enter integers for vertices and edges."
    return render_template("index.html")

@app.route("/result", methods=["POST"])
def result():
    try:
        V = int(request.form["vertices"])
        edges = []
        for i in range(int(request.form["edges"])):
            u = int(request.form[f"u{i}"])
            v = int(request.form[f"v{i}"])
            w = float(request.form[f"w{i}"])
            edges.append((u, v, w))

        # اجرای الگوریتم بلمن-فورد
        distances, cycles = bellman_ford_with_cycles(edges, V)

        # رسم گراف
        draw_graph(edges, V)

        return render_template(
            "result.html",
            vertices=V,
            edges=edges,
            distances=distances,
            cycles=cycles,
            graph_image="/static/graph.png",
        )
    except ValueError:
        return "Invalid input. Please ensure all fields are filled correctly."

def bellman_ford_with_cycles(graph, V):
    distance = [float("Inf")] * V
    predecessor = [-1] * V
    distance[0] = 0
    for _ in range(V - 1):
        for u, v, w in graph:
            if distance[u] != float("Inf") and distance[u] + w < distance[v]:
                distance[v] = distance[u] + w
                predecessor[v] = u
    cycles = []
    for u, v, w in graph:
        if distance[u] != float("Inf") and distance[u] + w < distance[v]:
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
            cycles.append(cycle[::-1])
    if cycles:
        return None, cycles
    return distance, cycles

def draw_graph(edges, V):
    G = nx.DiGraph()
    G.add_weighted_edges_from(edges)
    pos = nx.spring_layout(G)
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color="lightblue", edge_color="black", node_size=2000, font_size=15)
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): f"{w}" for u, v, w in edges})
    plt.savefig("static/graph.png")
    plt.close()

if __name__ == "__main__":
    if not os.path.exists("static"):
        os.makedirs("static")
    app.run(debug=True)





def read_graph_from_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    V = int(lines[0].split()[1])
    source = int(lines[1].split()[1])
    graph = []

    for line in lines[3:]:
        u, v, w = map(int, line.split())
        graph.append((u, v, w))

    return V, source, graph


def bellman_ford_with_cycles(graph, V, source):
    distance = [float("Inf")] * V
    predecessor = [-1] * V

    distance[source] = 0

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
                f"Negative weight cycle detected involving edge ({u}, {v}) with weight {w}.")

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

    print("Shortest distances from source:")
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
V, source, graph = read_graph_from_file(filename)


result = bellman_ford_with_cycles(graph, V, source)
