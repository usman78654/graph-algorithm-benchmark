import heapq
import matplotlib.pyplot as plt
import time

INPUT_TSV = 'soc-redditHyperlinks-body.tsv'
PRIM_OUT = 'mst_prim.txt'
KRUSKAL_OUT = 'mst_kruskal.txt'
AVG_DEG_OUT = 'average_degree.txt'

def load_graph(path):
    adj = {}
    edges = set()
    with open(path, 'r', encoding='utf-8') as f:
        header = next(f)
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) < 6:
                continue
            u, v = parts[0], parts[1]
            props = parts[5]
            try:
                weight = float(props.split(',')[0])
            except Exception:
                weight = 1.0
            adj.setdefault(u, []).append((v, weight))
            adj.setdefault(v, []).append((u, weight))
  
            if u < v:
                edges.add((u, v, weight))
            else:
                edges.add((v, u, weight))
    return adj, list(edges)

def prim_mst(adj):
    if not adj:
        return []
    start = next(iter(adj))
    visited = {start}
    heap = []
    for v, w in adj[start]:
        heapq.heappush(heap, (w, start, v))
    mst = []
    while heap and len(visited) < len(adj):
        w, u, v = heapq.heappop(heap)
        if v in visited:
            continue
        visited.add(v)
        mst.append((u, v, w))
        for nbr, wt in adj[v]:
            if nbr not in visited:
                heapq.heappush(heap, (wt, v, nbr))
    return mst

class UnionFind:
    def __init__(self, elements):
        self.parent = {e: e for e in elements}
    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x
    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[rb] = ra

def kruskal_mst(nodes, edges):
    uf = UnionFind(nodes)
    mst = []
    for u, v, w in sorted(edges, key=lambda e: e[2]):
        if uf.find(u) != uf.find(v):
            uf.union(u, v)
            mst.append((u, v, w))
    return mst

def compute_average_degree(adj, edges):
    num_nodes = len(adj)
    num_edges = len(edges)
    if num_nodes == 0:
        return 0.0

    return (2.0 * num_edges) / num_nodes

def write_edges(edges, path):
    with open(path, 'w', encoding='utf-8') as f:
        for u, v, w in edges:
            f.write(f"{u}\t{v}\t{w}\n")

def write_average_degree(avg_deg, path):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(f"Average Degree: {avg_deg:.4f}\n")

def plot_execution_times(sizes, prim_times, kruskal_times, deg_times, filename="execution_time_plot.png"):
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, prim_times, marker='o', label='Prim MST')
    plt.plot(sizes, kruskal_times, marker='s', label='Kruskal MST')
    plt.plot(sizes, deg_times, marker='^', label='Average Degree')
    plt.xlabel("Number of Nodes")
    plt.ylabel("Execution Time (seconds)")
    plt.title("Execution Time vs Graph Size")
    plt.legend()
    plt.grid(True)
    plt.savefig(filename)
    plt.close()
    print(f"[PLOT] Execution time plot saved to {filename}")

def plot_mst_weights(prim_edges, kruskal_edges, filename="mst_weight_comparison.png"):
    prim_total = sum(w for _, _, w in prim_edges)
    kruskal_total = sum(w for _, _, w in kruskal_edges)
    plt.bar(['Prim', 'Kruskal'], [prim_total, kruskal_total])
    plt.ylabel("Total MST Weight")
    plt.title("MST Total Weight Comparison")
    plt.savefig(filename)
    plt.close()
    print(f"[PLOT] MST weight comparison saved to {filename}")

if __name__ == '__main__':
    print("Loading graph with weighted edges from PROPERTIES...")
    adjacency, edges = load_graph(INPUT_TSV)
    nodes = list(adjacency.keys())
    print(f"Graph loaded: {len(nodes)} nodes, {len(edges)} edges")

    print("Computing Prim MST...")
    prim_res = prim_mst(adjacency)
    write_edges(prim_res, PRIM_OUT)
    print(f"Prim MST -> {PRIM_OUT} ({len(prim_res)} edges)")

    print("Computing Kruskal MST...")
    kruskal_res = kruskal_mst(nodes, edges)
    write_edges(kruskal_res, KRUSKAL_OUT)
    print(f"Kruskal MST -> {KRUSKAL_OUT} ({len(kruskal_res)} edges)")

    print("Computing average degree...")
    avg_deg = compute_average_degree(adjacency, edges)
    write_average_degree(avg_deg, AVG_DEG_OUT)
    print(f"Average degree -> {AVG_DEG_OUT}: {avg_deg:.4f}")

    plot_mst_weights(prim_res, kruskal_res)

    sizes = []
    prim_times = []
    kruskal_times = []
    deg_times = []

    sample_sizes = [100, 300, 500, 1000, 2000]

    for size in sample_sizes:
        print(f"\n[INFO] Benchmarking subgraph of {size} nodes...")
        sub_nodes = nodes[:size]
        sub_adj = {u: [(v, w) for v, w in nbrs if v in sub_nodes]
                   for u, nbrs in adjacency.items() if u in sub_nodes}
        sub_edges = [(u, v, w) for u, v, w in edges if u in sub_nodes and v in sub_nodes]

        sizes.append(size)

        t0 = time.time()
        _ = prim_mst(sub_adj)
        prim_times.append(time.time() - t0)

        t0 = time.time()
        _ = kruskal_mst(sub_nodes, sub_edges)
        kruskal_times.append(time.time() - t0)

        t0 = time.time()
        _ = compute_average_degree(sub_adj, sub_edges)
        deg_times.append(time.time() - t0)

    plot_execution_times(sizes, prim_times, kruskal_times, deg_times)
