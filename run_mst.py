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

def plot_mst_weights(prim_edges, kruskal_edges, filename="mst_weight_comparison.png"):
    prim_total = sum(w for _, _, w in prim_edges)
    kruskal_total = sum(w for _, _, w in kruskal_edges)
    plt.figure(figsize=(8, 6))
    plt.bar(['Prim', 'Kruskal'], [prim_total, kruskal_total])
    plt.ylabel("Total MST Weight")
    plt.title("MST Total Weight Comparison")
    plt.savefig(filename)
    plt.close()
    print(f"[PLOT] MST weight comparison saved to {filename}")

if __name__ == '__main__':
    print("Loading graph with weighted edges...")
    adjacency, edges = load_graph(INPUT_TSV)
    nodes = list(adjacency.keys())
    print(f"Graph loaded: {len(nodes)} nodes, {len(edges)} edges")

    print("Computing Prim MST...")
    start_prim = time.time()
    prim_res = prim_mst(adjacency)
    prim_time = time.time() - start_prim
    write_edges(prim_res, PRIM_OUT)
    print(f"Prim MST -> {PRIM_OUT} ({len(prim_res)} edges) Time: {prim_time:.6f}s")

    print("Computing Kruskal MST...")
    start_kruskal = time.time()
    kruskal_res = kruskal_mst(nodes, edges)
    kruskal_time = time.time() - start_kruskal
    write_edges(kruskal_res, KRUSKAL_OUT)
    print(f"Kruskal MST -> {KRUSKAL_OUT} ({len(kruskal_res)} edges) Time: {kruskal_time:.6f}s")

    print("Computing average degree...")
    start_deg = time.time()
    avg_deg = compute_average_degree(adjacency, edges)
    deg_time = time.time() - start_deg
    write_average_degree(avg_deg, AVG_DEG_OUT)
    print(f"Average degree -> {AVG_DEG_OUT}: {avg_deg:.4f} Time: {deg_time:.6f}s")

    plot_mst_weights(prim_res, kruskal_res)

    # Save execution times
    with open("prim_kruskal_executionTimes.txt", "w") as f:
        f.write(f"Prim MST execution time: {prim_time:.6f} seconds\n")
        f.write(f"Kruskal MST execution time: {kruskal_time:.6f} seconds\n")
        f.write(f"Average Degree execution time: {deg_time:.6f} seconds\n")

    print("\nAll algorithms completed!")
