import csv
import heapq
import time
import matplotlib.pyplot as plt

def load_graph_from_tsv(file_path):
    graph = {}
    nodes = set()

    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            src = row['SOURCE_SUBREDDIT']
            tgt = row['TARGET_SUBREDDIT']
            try:
                weight = abs(float(row['LINK_SENTIMENT']))
            except ValueError:
                continue
            if src not in graph:
                graph[src] = []
            graph[src].append((tgt, weight))
            nodes.update([src, tgt])

    return graph, list(nodes)

def dijkstra(graph, source, nodes):
    dist = {node: float('inf') for node in nodes}
    prev = {node: None for node in nodes}
    dist[source] = 0
    heap = [(0, source)]

    while heap:
        current_dist, u = heapq.heappop(heap)
        if current_dist > dist[u]:
            continue
        for v, weight in graph.get(u, []):
            if v not in dist:
                continue
            if dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                prev[v] = u
                heapq.heappush(heap, (dist[v], v))

    return dist, prev

def bellman_ford(graph, source, nodes):
    dist = {node: float('inf') for node in nodes}
    prev = {node: None for node in nodes}
    dist[source] = 0

    for _ in range(len(nodes) - 1):
        updated = False
        for u in graph:
            if u not in dist:
                continue
            for v, w in graph[u]:
                if v not in dist:
                    continue
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    prev[v] = u
                    updated = True
        if not updated:
            break

    for u in graph:
        if u not in dist:
            continue
        for v, w in graph[u]:
            if v not in dist:
                continue
            if dist[u] + w < dist[v]:
                raise ValueError("Graph contains a negative-weight cycle")

    return dist, prev

def reconstruct_path(prev, node):
    path = []
    while node is not None:
        path.insert(0, node)
        node = prev[node]
    return path

def measure_times(graph, nodes, input_sizes, source):
    dijkstra_times = []
    bellman_times = []

    for size in input_sizes:
        subset = set(nodes[:size])
        if source not in subset:
            subset.add(source)

        print(f"Running for input size: {size}")

        start = time.time()
        dijkstra(graph, source, subset)
        dijkstra_times.append(time.time() - start)

        start = time.time()
        bellman_ford(graph, source, subset)
        bellman_times.append(time.time() - start)

    return dijkstra_times, bellman_times


def plot_execution_times(input_sizes, dijkstra_times, bellman_times):
    plt.figure(figsize=(10, 6))
    plt.plot(input_sizes, dijkstra_times, marker='o', label='Dijkstra')
    plt.plot(input_sizes, bellman_times, marker='s', label='Bellman-Ford')
    plt.xlabel('Number of Nodes')
    plt.ylabel('Execution Time (seconds)')
    plt.title('Execution Time vs Number of Nodes')
    plt.legend()
    plt.grid(True)
    plt.savefig('execution_time_plot.png')
    plt.show()

if __name__ == "__main__":
    file_path = "soc-redditHyperlinks-body.tsv"
    graph, nodes = load_graph_from_tsv(file_path)
    
    # Allow user to select source node
    source = input("Enter source subreddit (or press Enter for 'leagueoflegends'): ").strip()
    if not source:
        source = "leagueoflegends"
    
    if source not in graph:
        print(f"Warning: '{source}' not found in graph. Using first available node.")
        source = next(iter(graph), "leagueoflegends")

    # --- Dijkstra ---
    print("\n--- Dijkstra ---")
    start_time = time.time()
    dist_d, prev_d = dijkstra(graph, source, nodes)
    dijkstra_time = time.time() - start_time
    print(f"Dijkstra execution time: {dijkstra_time:.6f} seconds")

    with open("dijkstra_paths.txt", "w", encoding="utf-8") as f:
        f.write(f"Source: {source}\n")
        f.write(f"Execution Time: {dijkstra_time:.6f} seconds\n")
        f.write(f"{'='*80}\n")
        for node in dist_d:
            if dist_d[node] < float('inf'):
                path = reconstruct_path(prev_d, node)
                line = f"{source} -> {node}: distance = {dist_d[node]}, path = {path}"
                print(line)
                f.write(line + "\n")

    # --- Bellman-Ford ---
    print("\n--- Bellman-Ford ---")
    start_time = time.time()
    dist_b, prev_b = bellman_ford(graph, source, nodes)
    bellman_ford_time = time.time() - start_time
    print(f"Bellman-Ford execution time: {bellman_ford_time:.6f} seconds")

    with open("bellman_ford_paths.txt", "w", encoding="utf-8") as f:
        f.write(f"Source: {source}\n")
        f.write(f"Execution Time: {bellman_ford_time:.6f} seconds\n")
        f.write(f"{'='*80}\n")
        for node in dist_b:
            if dist_b[node] < float('inf'):
                path = reconstruct_path(prev_b, node)
                line = f"{source} -> {node}: distance = {dist_b[node]}, path = {path}"
                print(line)
                f.write(line + "\n")
    
    # Save execution times
    with open("dijkstra_bellman_executionTimes.txt", "w") as f:
        f.write(f"Dijkstra execution time: {dijkstra_time:.6f} seconds\n")
        f.write(f"Bellman-Ford execution time: {bellman_ford_time:.6f} seconds\n")

    # Store execution times
    with open("ShortestPath_execution_times.txt", "w", encoding="utf-8") as f:
        f.write(f"Dijkstra execution time: {dijkstra_time:.4f} seconds\n")
        f.write(f"Bellman-Ford execution time: {bellman_ford_time:.4f} seconds\n")

    input_sizes = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
    dijkstra_times, bellman_times = measure_times(graph, nodes, input_sizes, source)
    plot_execution_times(input_sizes, dijkstra_times, bellman_times)
