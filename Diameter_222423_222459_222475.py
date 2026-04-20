import csv
import heapq
import time

def load_graph_from_tsv(file_path):
    graph = {}
    reverse_graph = {}
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
            if tgt not in reverse_graph:
                reverse_graph[tgt] = []
            reverse_graph[tgt].append(src)
            nodes.update([src, tgt])

    connected_nodes = {n for n in nodes if n in graph or n in reverse_graph}
    return graph, connected_nodes

def dijkstra(graph, source, nodes, memo):
    if source in memo:
        return memo[source]

    dist = {node: float('inf') for node in nodes}
    dist[source] = 0
    heap = [(0, source)]

    while heap:
        current_dist, u = heapq.heappop(heap)
        if current_dist > dist[u]:
            continue
        for v, weight in graph.get(u, []):
            alt = dist[u] + weight
            if alt < dist[v]:
                dist[v] = alt
                heapq.heappush(heap, (alt, v))

    memo[source] = dist
    return dist

def compute_diameter(graph, nodes, limit=1500):
    diameter = 0
    memo = {}
    nodes_to_process = list(nodes)[:limit]

    with open("diameter_trace.txt", "w", encoding="utf-8") as trace_file:
        trace_file.write(f"Calculating diameter using the first {limit} nodes...\n")
        print(f"Calculating the diameter of the graph using the first {limit} nodes...")

        for idx, node in enumerate(nodes_to_process):
            log_line = f"Processing node {idx + 1}/{len(nodes_to_process)}: {node}"
            print(log_line)
            trace_file.write(log_line + "\n")

            dist = dijkstra(graph, node, nodes, memo)
            local_max = max((d for d in dist.values() if d < float('inf')), default=0)
            trace_file.write(f"Max distance from {node}: {local_max}\n")
            diameter = max(diameter, local_max)

        trace_file.write(f"\nFinal computed diameter: {diameter}\n")

    return diameter

if __name__ == "__main__":
    file_path = "soc-redditHyperlinks-body.tsv"
    graph, nodes = load_graph_from_tsv(file_path)

    # Allow user to select a starting node (for diameter calculation)
    start_node = input("Enter a starting subreddit for diameter calculation (or press Enter to use first node): ").strip()
    if not start_node or start_node not in graph:
        start_node = next(iter(nodes), None)
        if start_node:
            print(f"Using starting node: {start_node}")

    start_time = time.time()
    diameter = compute_diameter(graph, nodes, limit=500)
    elapsed = time.time() - start_time

    print(f"\nGraph diameter: {diameter}")
    print(f"Computation time: {elapsed:.6f} seconds")

    with open("diameter_result.txt", "w", encoding="utf-8") as f:
        f.write(f"Graph Diameter: {diameter}\n")
        f.write(f"Computation Time: {elapsed:.6f} seconds\n")
        f.write(f"Nodes processed: 500\n")
    
    with open("execution_times.txt", "a", encoding="utf-8") as f:
        f.write(f"Diameter computation time: {elapsed:.6f} seconds\n")
