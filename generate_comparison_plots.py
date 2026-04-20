import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from datetime import datetime

# Execution time data from actual runs
bfs_dfs_data = {
    'BFS': 0.056346,
    'DFS': 0.071730,
    'Cycle Detection': 0.000061
}

shortest_path_data = {
    'Dijkstra': 0.129538,
    'Bellman-Ford': 0.487246
}

mst_data = {
    'Prim': 0.798253,
    'Kruskal': 0.419826,
    'Avg Degree': 0.000008
}

diameter_data = {
    'Diameter (500 nodes)': 47.057217
}

all_algorithms = {
    'Cycle Detection': 0.000061,
    'Avg Degree': 0.000008,
    'BFS': 0.056346,
    'DFS': 0.071730,
    'Dijkstra': 0.129538,
    'Kruskal': 0.419826,
    'Prim': 0.798253,
    'Bellman-Ford': 0.487246,
    'Diameter': 47.057217
}

# Create comprehensive plots
fig = plt.figure(figsize=(18, 12))

# Plot 1: Graph Traversal Comparison
ax1 = plt.subplot(2, 3, 1)
algos = list(bfs_dfs_data.keys())
times = list(bfs_dfs_data.values())
colors1 = ['#3498db', '#e74c3c', '#2ecc71']
bars1 = ax1.bar(algos, times, color=colors1, edgecolor='black', linewidth=1.5)
ax1.set_ylabel('Execution Time (seconds)', fontsize=11, fontweight='bold')
ax1.set_title('Graph Traversal Algorithms', fontsize=12, fontweight='bold')
ax1.set_yscale('log')
ax1.grid(axis='y', alpha=0.3, linestyle='--')
for i, bar in enumerate(bars1):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
            f'{times[i]:.6f}s', ha='center', va='bottom', fontsize=9, fontweight='bold')
ax1.tick_params(axis='x', rotation=15)

# Plot 2: Shortest Path Algorithms Comparison
ax2 = plt.subplot(2, 3, 2)
algos = list(shortest_path_data.keys())
times = list(shortest_path_data.values())
colors2 = ['#9b59b6', '#f39c12']
bars2 = ax2.bar(algos, times, color=colors2, edgecolor='black', linewidth=1.5)
ax2.set_ylabel('Execution Time (seconds)', fontsize=11, fontweight='bold')
ax2.set_title('Shortest Path Algorithms', fontsize=12, fontweight='bold')
ax2.grid(axis='y', alpha=0.3, linestyle='--')
for i, bar in enumerate(bars2):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
            f'{times[i]:.6f}s', ha='center', va='bottom', fontsize=9, fontweight='bold')
speedup = shortest_path_data['Bellman-Ford'] / shortest_path_data['Dijkstra']
ax2.text(0.5, max(times)*0.7, f'Dijkstra {speedup:.2f}x faster', 
         ha='center', fontsize=10, bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
ax2.tick_params(axis='x', rotation=15)

# Plot 3: MST Algorithms Comparison
ax3 = plt.subplot(2, 3, 3)
algos = list(mst_data.keys())
times = list(mst_data.values())
colors3 = ['#16a085', '#27ae60', '#1abc9c']
bars3 = ax3.bar(algos, times, color=colors3, edgecolor='black', linewidth=1.5)
ax3.set_ylabel('Execution Time (seconds)', fontsize=11, fontweight='bold')
ax3.set_title('Minimum Spanning Tree Algorithms', fontsize=12, fontweight='bold')
ax3.set_yscale('log')
ax3.grid(axis='y', alpha=0.3, linestyle='--')
for i, bar in enumerate(bars3):
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2., height,
            f'{times[i]:.6f}s', ha='center', va='bottom', fontsize=8, fontweight='bold')
speedup_mst = mst_data['Prim'] / mst_data['Kruskal']
ax3.text(0.5, max(times)*0.5, f'Kruskal {speedup_mst:.2f}x faster', 
         ha='center', fontsize=10, bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.7))
ax3.tick_params(axis='x', rotation=15)

# Plot 4: All Algorithms Comparison (Log Scale)
ax4 = plt.subplot(2, 3, 4)
algos_all = list(all_algorithms.keys())
times_all = list(all_algorithms.values())
colors_all = ['#2ecc71', '#1abc9c', '#3498db', '#e74c3c', '#9b59b6', '#f39c12', '#16a085', '#e67e22', '#c0392b']
bars4 = ax4.barh(algos_all, times_all, color=colors_all, edgecolor='black', linewidth=1.5)
ax4.set_xlabel('Execution Time (seconds - Log Scale)', fontsize=11, fontweight='bold')
ax4.set_title('All Algorithms Performance Comparison', fontsize=12, fontweight='bold')
ax4.set_xscale('log')
ax4.grid(axis='x', alpha=0.3, linestyle='--')
for i, bar in enumerate(bars4):
    width = bar.get_width()
    ax4.text(width*1.2, bar.get_y() + bar.get_height()/2.,
            f'{times_all[i]:.4f}s', ha='left', va='center', fontsize=9, fontweight='bold')

# Plot 5: Algorithm Category Comparison
ax5 = plt.subplot(2, 3, 5)
categories = ['Traversal\n(BFS/DFS)', 'Shortest Path\n(Dijkstra)', 'MST\n(Kruskal)', 'Cycle\nDetection', 'Diameter']
category_times = [0.056346, 0.129538, 0.419826, 0.000061, 47.057217]
colors5 = ['#3498db', '#9b59b6', '#16a085', '#2ecc71', '#e74c3c']
bars5 = ax5.bar(categories, category_times, color=colors5, edgecolor='black', linewidth=1.5)
ax5.set_ylabel('Execution Time (seconds)', fontsize=11, fontweight='bold')
ax5.set_title('Algorithm Categories Performance', fontsize=12, fontweight='bold')
ax5.set_yscale('log')
ax5.grid(axis='y', alpha=0.3, linestyle='--')
for i, bar in enumerate(bars5):
    height = bar.get_height()
    ax5.text(bar.get_x() + bar.get_width()/2., height,
            f'{category_times[i]:.2f}s', ha='center', va='bottom', fontsize=9, fontweight='bold')

# Plot 6: Speedup Analysis
ax6 = plt.subplot(2, 3, 6)
speedup_labels = ['DFS vs BFS', 'Bellman-Ford\nvs Dijkstra', 'Prim vs\nKruskal']
speedup_values = [bfs_dfs_data['DFS']/bfs_dfs_data['BFS'], 
                  shortest_path_data['Bellman-Ford']/shortest_path_data['Dijkstra'],
                  mst_data['Prim']/mst_data['Kruskal']]
colors6 = ['#e74c3c', '#f39c12', '#3498db']
bars6 = ax6.bar(speedup_labels, speedup_values, color=colors6, edgecolor='black', linewidth=1.5)
ax6.axhline(y=1, color='red', linestyle='--', linewidth=2, label='No Speedup (1x)')
ax6.set_ylabel('Speedup Factor (X times faster)', fontsize=11, fontweight='bold')
ax6.set_title('Algorithm Speedup Comparison', fontsize=12, fontweight='bold')
ax6.grid(axis='y', alpha=0.3, linestyle='--')
for i, bar in enumerate(bars6):
    height = bar.get_height()
    if speedup_values[i] > 1:
        ax6.text(bar.get_x() + bar.get_width()/2., height,
                f'{speedup_values[i]:.2f}x', ha='center', va='bottom', fontsize=10, fontweight='bold', color='green')
    else:
        ax6.text(bar.get_x() + bar.get_width()/2., height,
                f'{speedup_values[i]:.2f}x', ha='center', va='bottom', fontsize=10, fontweight='bold', color='red')

plt.suptitle('Algorithm Execution Time Analysis - Reddit Hyperlinks Dataset\n(35,776 nodes, 281,229 edges)', 
             fontsize=14, fontweight='bold', y=0.995)
plt.tight_layout()
plt.savefig('algorithm_performance_comparison.png', dpi=300, bbox_inches='tight')
print("✓ Saved: algorithm_performance_comparison.png")
plt.close()

# Create a second figure with scalability analysis
fig2, axes = plt.subplots(2, 2, figsize=(16, 10))

# Simulated scalability data based on complexity
node_counts = np.array([1000, 5000, 10000, 20000, 35776])

# BFS/DFS: O(V+E) - Linear
bfs_expected = 0.056346 * (node_counts / 35776) * (node_counts / 35776 * 7.85)  # Approximate edge ratio
dfs_expected = 0.071730 * (node_counts / 35776) * (node_counts / 35776 * 7.85)

# Dijkstra: O((V+E)logV)
dijkstra_expected = 0.129538 * (node_counts / 35776) * np.log(node_counts) / np.log(35776)

# Bellman-Ford: O(V*E)
bellman_expected = 0.487246 * (node_counts / 35776) ** 2

# Kruskal: O(E log E)
kruskal_expected = 0.419826 * (node_counts / 35776) ** 1.5

# Prim: O(V log E)
prim_expected = 0.798253 * (node_counts / 35776) * np.log(node_counts) / np.log(35776)

# Plot 1: Graph Traversal Scalability
ax1 = axes[0, 0]
ax1.plot(node_counts, bfs_expected, 'o-', linewidth=2.5, markersize=8, label='BFS O(V+E)', color='#3498db')
ax1.plot(node_counts, dfs_expected, 's-', linewidth=2.5, markersize=8, label='DFS O(V+E)', color='#e74c3c')
ax1.scatter([35776], [0.056346], color='#3498db', s=200, zorder=5, edgecolors='black', linewidth=2)
ax1.scatter([35776], [0.071730], color='#e74c3c', s=200, zorder=5, edgecolors='black', linewidth=2)
ax1.set_xlabel('Number of Nodes', fontsize=11, fontweight='bold')
ax1.set_ylabel('Execution Time (seconds)', fontsize=11, fontweight='bold')
ax1.set_title('Graph Traversal Scalability', fontsize=12, fontweight='bold')
ax1.legend(fontsize=10, loc='upper left')
ax1.grid(True, alpha=0.3, linestyle='--')

# Plot 2: Shortest Path Scalability
ax2 = axes[0, 1]
ax2.plot(node_counts, dijkstra_expected, 'o-', linewidth=2.5, markersize=8, label='Dijkstra O((V+E)logV)', color='#9b59b6')
ax2.plot(node_counts, bellman_expected, 's-', linewidth=2.5, markersize=8, label='Bellman-Ford O(V*E)', color='#f39c12')
ax2.scatter([35776], [0.129538], color='#9b59b6', s=200, zorder=5, edgecolors='black', linewidth=2)
ax2.scatter([35776], [0.487246], color='#f39c12', s=200, zorder=5, edgecolors='black', linewidth=2)
ax2.set_xlabel('Number of Nodes', fontsize=11, fontweight='bold')
ax2.set_ylabel('Execution Time (seconds)', fontsize=11, fontweight='bold')
ax2.set_title('Shortest Path Scalability', fontsize=12, fontweight='bold')
ax2.legend(fontsize=10, loc='upper left')
ax2.grid(True, alpha=0.3, linestyle='--')

# Plot 3: MST Scalability
ax3 = axes[1, 0]
ax3.plot(node_counts, kruskal_expected, 'o-', linewidth=2.5, markersize=8, label='Kruskal O(E log E)', color='#16a085')
ax3.plot(node_counts, prim_expected, 's-', linewidth=2.5, markersize=8, label='Prim O(V log E)', color='#27ae60')
ax3.scatter([35776], [0.419826], color='#16a085', s=200, zorder=5, edgecolors='black', linewidth=2)
ax3.scatter([35776], [0.798253], color='#27ae60', s=200, zorder=5, edgecolors='black', linewidth=2)
ax3.set_xlabel('Number of Nodes', fontsize=11, fontweight='bold')
ax3.set_ylabel('Execution Time (seconds)', fontsize=11, fontweight='bold')
ax3.set_title('MST Algorithms Scalability', fontsize=12, fontweight='bold')
ax3.legend(fontsize=10, loc='upper left')
ax3.grid(True, alpha=0.3, linestyle='--')

# Plot 4: Complexity Class Comparison
ax4 = axes[1, 1]
ax4.plot(node_counts, node_counts, 'o-', linewidth=2.5, markersize=8, label='O(n) - Linear', color='#2ecc71')
ax4.plot(node_counts, node_counts * np.log(node_counts) / np.log(35776), 's-', linewidth=2.5, markersize=8, 
         label='O(n log n) - Log Linear', color='#3498db')
ax4.plot(node_counts, node_counts**1.5, '^-', linewidth=2.5, markersize=8, label='O(n^1.5)', color='#f39c12')
ax4.plot(node_counts, node_counts**2 / 100, 'D-', linewidth=2.5, markersize=8, label='O(n²) / 100', color='#e74c3c')
ax4.set_xlabel('Number of Nodes (n)', fontsize=11, fontweight='bold')
ax4.set_ylabel('Relative Execution Time', fontsize=11, fontweight='bold')
ax4.set_title('Complexity Classes Growth Rates', fontsize=12, fontweight='bold')
ax4.legend(fontsize=10, loc='upper left')
ax4.grid(True, alpha=0.3, linestyle='--')
ax4.set_yscale('log')

plt.suptitle('Algorithm Scalability Analysis with Different Input Sizes\n(Projected performance based on complexity classes)', 
             fontsize=14, fontweight='bold', y=0.995)
plt.tight_layout()
plt.savefig('algorithm_scalability_analysis.png', dpi=300, bbox_inches='tight')
print("✓ Saved: algorithm_scalability_analysis.png")
plt.close()

# Create summary statistics
print("\n" + "="*70)
print("EXECUTION TIME ANALYSIS SUMMARY")
print("="*70)
print(f"\nDataset: soc-redditHyperlinks-body.tsv")
print(f"Nodes: 35,776 | Edges: 281,229")
print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"\n{'Algorithm':<25} {'Time (sec)':<15} {'Complexity':<20}")
print("-" * 70)
for algo, time in sorted(all_algorithms.items(), key=lambda x: x[1]):
    if 'BFS' in algo:
        complexity = "O(V+E)"
    elif 'DFS' in algo:
        complexity = "O(V+E)"
    elif 'Dijkstra' in algo:
        complexity = "O((V+E)logV)"
    elif 'Bellman' in algo:
        complexity = "O(V*E)"
    elif 'Kruskal' in algo:
        complexity = "O(ElogE)"
    elif 'Prim' in algo:
        complexity = "O(VlogE)"
    elif 'Cycle' in algo:
        complexity = "O(V+E)"
    elif 'Avg' in algo:
        complexity = "O(1)"
    elif 'Diameter' in algo:
        complexity = "O(V³)"
    else:
        complexity = "N/A"
    print(f"{algo:<25} {time:<15.6f} {complexity:<20}")
print("="*70)
