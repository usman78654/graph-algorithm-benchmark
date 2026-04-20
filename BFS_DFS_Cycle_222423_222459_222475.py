
import time
import random
import matplotlib.pyplot as plt
from collections import deque

dataset_tsv    = 'soc-redditHyperlinks-body.tsv'
order_bfs      = 'bfs_order.txt'
order_dfs      = 'dfs_order.txt'
cycle_save    = 'cycle.txt'
trace_bfs    = 'trace_bfs.txt'
trace_dfs    = 'trace_dfs.txt'

def loadGraph(path):
    adjacencyList = {}
    file = open(path, 'r', encoding='utf-8')
    for line in file:
        line = line.strip()
        if line == ''or line.startswith('#'):
            continue
        parts = line.split()
        if len(parts) < 2:
            continue
        if parts[0].lower().startswith('source_subreddit'):
            continue
        u, v = parts[0], parts[1]
        if u not in adjacencyList:
            adjacencyList[u] = []
        adjacencyList[u].append(v)
        if v not in adjacencyList:
            adjacencyList[v] = []
    file.close()
    return adjacencyList



def bfsTraversal(adjacencyList, source):
    visitedNodes = set([source])
    queue = deque([source])
    visitOrder = []
    trace = []
    trace.append(f"enqueue {source}")
    while len(queue) > 0:
        current = queue.popleft()
        trace.append(f"dequeue {current}")
        visitOrder.append(current)
        neighbors = adjacencyList[current]
        for neighbor in neighbors:
            if neighbor not in visitedNodes:
                visitedNodes.add(neighbor)
                queue.append(neighbor)
                trace.append(f"enqueue {neighbor}")
    return visitOrder, trace

def dfsTraversal(adjacencyList, source):
    visitedNodes = set()
    stack = [source]
    visitOrder = []
    trace = []
    trace.append(f"push {source}")

    while len(stack) > 0:
        current = stack.pop()
        trace.append(f"pop {current}")
        if current in visitedNodes:
            continue
        visitedNodes.add(current)
        visitOrder.append(current)
        neighbors = adjacencyList[current]
        i = len(neighbors) - 1
        while i >= 0:
            neighbor = neighbors[i]
            if neighbor not in visitedNodes:
                stack.append(neighbor)
                trace.append(f"push {neighbor}")
            i -= 1

    return visitOrder, trace

def findCycle(adjacencyList):
    visitedNodes = set()
    recursionStack = set()
    pathStack = []
    cycleNodes = []

    def visit(node):
        visitedNodes.add(node)
        recursionStack.add(node)
        pathStack.append(node)
        for neighbor in adjacencyList[node]:
            if neighbor not in visitedNodes:
                if visit(neighbor):
                    return True
            elif neighbor in recursionStack:
                idx = 0
                while pathStack[idx] != neighbor:
                    idx += 1
                for j in range(idx, len(pathStack)):
                    cycleNodes.append(pathStack[j])
                return True
        recursionStack.remove(node)
        pathStack.pop()
        return False

    for n in adjacencyList:
        if n not in visitedNodes:
            if visit(n):
                return True, cycleNodes
    return False, []

def writeList(items, path):
    file = open(path, 'w', encoding='utf-8')
    for x in items:
        file.write(x + '\n')
    file.close()




def generateRandomGraph(num_nodes, num_edges, directed=False):
    adjacencyList = {str(i): [] for i in range(num_nodes)}
    edge_set = set()

    while len(edge_set) < num_edges:
        u = str(random.randint(0, num_nodes - 1))
        v = str(random.randint(0, num_nodes - 1))
        if u == v or (u, v) in edge_set:
            continue
        adjacencyList[u].append(v)
        edge_set.add((u, v))
        if not directed:
            adjacencyList[v].append(u)
            edge_set.add((v, u))
    return adjacencyList




def benchmarkAndPlot():
    node_sizes = [1000,2000,3000,4000,5000,6000,7000,8000,9000,10000]
    bfs_times = []
    dfs_times = []
    cycle_times = []

    for n in node_sizes:
        e_sparse = n * 2
        e_dense = n * (n//100)

        for edges, density_label in [(e_sparse, 'sparse'), (e_dense, 'dense')]:
            graph = generateRandomGraph(n, edges, directed=True)
            source = '0'

            start = time.time()
            bfsTraversal(graph, source)
            end = time.time()
            bfs_times.append((n, density_label, end - start))

            start = time.time()
            dfsTraversal(graph, source)
            end = time.time()
            dfs_times.append((n, density_label, end - start))

            start = time.time()
            findCycle(graph)
            end = time.time()
            cycle_times.append((n, density_label, end - start))


    def plot_times(times, label):
        sparse_x = [n for n, d, _ in times if d == 'sparse']
        sparse_y = [t for n, d, t in times if d == 'sparse']
        dense_x = [n for n, d, _ in times if d == 'dense']
        dense_y = [t for n, d, t in times if d == 'dense']
        plt.plot(sparse_x, sparse_y, label=f'{label} (sparse)', marker='o')
        plt.plot(dense_x, dense_y, label=f'{label} (dense)', marker='x')

    plt.figure(figsize=(12, 6))
    plot_times(bfs_times, 'BFS')
    plot_times(dfs_times, 'DFS')
    plot_times(cycle_times, 'Cycle Detection')
    plt.xlabel("Number of Nodes")
    plt.ylabel("Execution Time (seconds)")
    plt.title("Execution Time vs Graph Size for BFS, DFS, and Cycle Detection")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("execution_times_plot.png")
    plt.show()





def main():
    graph = loadGraph(dataset_tsv)
    if len(graph) == 0:
        print('Error: graph is empty')
        return

    sourceNode = input('Enter source subreddit: ')
    print('Using source:', sourceNode)
    start_B= time.time()
    bfsOrder, bfsTrace = bfsTraversal(graph, sourceNode)
    end_B=time.time()
 

    writeList(bfsOrder, order_bfs)
    writeList(bfsTrace, trace_bfs)
    print('BFS visited', len(bfsOrder), 'nodes ->', order_bfs)
    print('BFS trace written to', trace_bfs)

    start_D=time.time()
    dfsOrder, dfsTrace = dfsTraversal(graph, sourceNode)
    end_D=time.time()

    writeList(dfsOrder, order_dfs)
    writeList(dfsTrace, trace_dfs)
    print('DFS visited', len(dfsOrder), 'nodes ->', order_dfs)
    print('DFS trace written to', trace_dfs)

    
    start_C=time.time()
    hasCycle, cycleNodes = findCycle(graph)
    end_C=time.time()
    with open('BFS_DFS_executionTimes.txt', 'w') as f:
        f.write(f"BFS execution Time: {end_B-start_B:.6f} seconds\n")
        f.write(f"DFS execution Time: {end_D-start_D:.6f} seconds\n")
        f.write(f"Cycle Detection execution Time: {end_C-start_C:.6f} seconds\n")
    cycleFile = open(cycle_save, 'w', encoding='utf-8')
    cycleFile.write('Cycle detected: ' + str(hasCycle) + '\n')
    if hasCycle:
        cycleFile.write('Nodes in cycle:\n')
        for cn in cycleNodes:
            cycleFile.write(cn + '\n')
    cycleFile.close()
    print('Cycle detection ->', cycle_save)


    benchmarkAndPlot()

if __name__ == '__main__':
    main()
