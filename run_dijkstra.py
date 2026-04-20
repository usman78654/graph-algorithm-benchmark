import csv
import heapq
import time
import matplotlib.pyplot as plt
import sys

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

if __name__ == "__main__":
    file_path = "soc-redditHyperlinks-body.tsv"
    print("Loading graph...")
    graph, nodes = load_graph_from_tsv(file_path)
    
    source = "leagueoflegends"
    if source not in graph:
        source = next(iter(graph), None)
        print(f"Source not found, using: {source}")

    # --- Dijkstra ---
    print("\n--- Running Dijkstra ---")
    start_time = time.time()
    dist_d, prev_d = dijkstra(graph, source, nodes)
    dijkstra_time = time.time() - start_time
    print(f"Dijkstra execution time: {dijkstra_time:.6f} seconds")

    with open("dijkstra_paths.txt", "w", encoding="utf-8") as f:
        f.write(f"Source: {source}\n")
        f.write(f"Execution Time: {dijkstra_time:.6f} seconds\n")
        f.write(f"{'='*80}\n")
        count = 0
        for node in dist_d:
            if dist_d[node] < float('inf'):
                path = reconstruct_path(prev_d, node)
                line = f"{source} -> {node}: distance = {dist_d[node]}, path = {path}"
                if count < 100:
                    print(line)
                f.write(line + "\n")
                count += 1
        print(f"... ({count} total paths written)")

    # --- Bellman-Ford ---
    print("\n--- Running Bellman-Ford ---")
    start_time = time.time()
    dist_b, prev_b = bellman_ford(graph, source, nodes)
    bellman_ford_time = time.time() - start_time
    print(f"Bellman-Ford execution time: {bellman_ford_time:.6f} seconds")

    with open("bellman_ford_paths.txt", "w", encoding="utf-8") as f:
        f.write(f"Source: {source}\n")
        f.write(f"Execution Time: {bellman_ford_time:.6f} seconds\n")
        f.write(f"{'='*80}\n")
        count = 0
        for node in dist_b:
            if dist_b[node] < float('inf'):
                path = reconstruct_path(prev_b, node)
                line = f"{source} -> {node}: distance = {dist_b[node]}, path = {path}"
                if count < 100:
                    print(line)
                f.write(line + "\n")
                count += 1
        print(f"... ({count} total paths written)")
    
    # Save execution times
    with open("dijkstra_bellman_executionTimes.txt", "w") as f:
        f.write(f"Dijkstra execution time: {dijkstra_time:.6f} seconds\n")
        f.write(f"Bellman-Ford execution time: {bellman_ford_time:.6f} seconds\n")
    
    print("\nDone! Check dijkstra_paths.txt, bellman_ford_paths.txt, and dijkstra_bellman_executionTimes.txt")
