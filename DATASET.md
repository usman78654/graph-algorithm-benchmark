# Dataset Setup Instructions

## Overview

This project uses the **Reddit Hyperlinks Network** dataset from SNAP Stanford.

**File:** `soc-redditHyperlinks-body.tsv`  
**Size:** 304 MB  
**Nodes:** 35,776 subreddits  
**Edges:** 281,229 hyperlinks  

---

## Downloading the Dataset

The dataset is **not included in the repository** due to GitHub's 100 MB file size limit.

### Option 1: Direct Download (Recommended)

1. Download from SNAP Stanford: [http://snap.stanford.edu/data/soc-redditHyperlinks.html](http://snap.stanford.edu/data/soc-redditHyperlinks.html)

2. Extract the file `soc-redditHyperlinks-body.tsv`

3. Place it in the project root directory:
   ```
   graph-algorithm-benchmark/
   ├── soc-redditHyperlinks-body.tsv  ← Place here
   ├── README.md
   ├── BFS_DFS_Cycle_222423_222459_222475.py
   └── ...
   ```

### Option 2: Command Line Download

Using `wget` (if available):
```bash
wget http://snap.stanford.edu/data/soc-redditHyperlinks.tar.gz
tar -xzf soc-redditHyperlinks.tar.gz
cp soc-redditHyperlinks/soc-redditHyperlinks-body.tsv .
```

Using `curl`:
```bash
curl -O http://snap.stanford.edu/data/soc-redditHyperlinks.tar.gz
tar -xzf soc-redditHyperlinks.tar.gz
cp soc-redditHyperlinks/soc-redditHyperlinks-body.tsv .
```

---

## Dataset Format

The TSV file contains the following columns:

```
SOURCE_SUBREDDIT | TARGET_SUBREDDIT | POST_ID | TIMESTAMP | LINK_SENTIMENT | POST_PROPERTIES
```

### Column Details

1. **SOURCE_SUBREDDIT** - Origin subreddit (string)
2. **TARGET_SUBREDDIT** - Destination subreddit (string)
3. **POST_ID** - Reddit post identifier (integer)
4. **TIMESTAMP** - Unix timestamp of post creation (integer)
5. **LINK_SENTIMENT** - Link sentiment value: +1 (positive) or -1 (negative) (integer)
6. **POST_PROPERTIES** - 86-dimensional feature vector (comma-separated numbers)

### Example Row

```
leagueoflegends	gaming	t3_abc123	1234567890	1	0.85,0.92,0.78,...
```

---

## Verifying the Dataset

After placing the file in the project root, verify it:

```bash
# Check file size
ls -lh soc-redditHyperlinks-body.tsv

# Count lines
wc -l soc-redditHyperlinks-body.tsv
# Expected: ~286,562 lines (285,000 data rows + 1 header)

# Check first few lines
head -3 soc-redditHyperlinks-body.tsv
```

---

## Dataset Statistics

| Property | Value |
|----------|-------|
| **File Size** | 304 MB |
| **Nodes (Subreddits)** | 35,776 |
| **Edges (Hyperlinks)** | 281,229 |
| **Graph Density** | 0.000219 (sparse) |
| **Average Degree** | 15.72 |
| **Graph Diameter** | 12.0 |
| **Edge Direction** | Directed |
| **Edge Weights** | +1 or -1 (sentiment) |

---

## POST_PROPERTIES Format (86 dimensions)

The POST_PROPERTIES column contains 86 comma-separated numerical features:

1-8: Basic text properties (character count, word count, etc.)
9-40: LIWC linguistic dimensions
41-86: Extended text features

Example parsing in Python:
```python
props_str = "0.85,0.92,0.78,..."
props = list(map(float, props_str.split(',')))
# props is now a list of 86 floats
```

---

## Using the Dataset with the Project

Once the file is placed in the project root, all scripts will automatically load it:

```bash
# Run BFS/DFS
python BFS_DFS_Cycle_222423_222459_222475.py

# Run Dijkstra/Bellman-Ford
python run_dijkstra.py

# Run MST algorithms
python run_mst.py

# Calculate diameter
python run_diameter.py
```

---

## Citation

If you use this dataset in research, please cite:

```
McAuley, J., Targett, C., Shi, Q., & Van Den Hengel, A. (2015).
"Image-based recommendations on style and substance."
Proceedings of the 21st ACM SIGKDD International Conference on Knowledge Discovery and Data Mining.
```

**Dataset Source:** [SNAP - Stanford Network Analysis Project](http://snap.stanford.edu/data/index.html)

---

## Troubleshooting

### File Not Found Error
```
Error: cannot open file 'soc-redditHyperlinks-body.tsv'
```
**Solution:** Make sure the TSV file is in the same directory as the Python scripts.

### Encoding Error
```
UnicodeDecodeError: 'utf-8' codec can't decode byte...
```
**Solution:** The file may have encoding issues. Try specifying encoding in Python:
```python
with open('soc-redditHyperlinks-body.tsv', 'r', encoding='utf-8', errors='ignore') as f:
    reader = csv.DictReader(f, delimiter='\t')
```

### File Size Too Large
```
MemoryError: Unable to allocate 50 GB for an array...
```
**Solution:** The algorithms use streaming/iterative processing, but if loading entire graph fails:
- Use a smaller subset of the data
- Process in chunks
- Use external databases (Neo4j, NetworkX with streaming)

---

## Alternative Datasets

For testing with smaller datasets, try:
- `soc-redditHyperlinks-title.tsv` - Smaller version with title-based links
- `soc-Slashdot0811.txt` - 77K nodes, smaller
- `soc-Epinions1.txt` - 75K nodes
- `web-Google.txt` - 875K nodes

All available at [SNAP Stanford](http://snap.stanford.edu/data/index.html)

---

**Setup Complete!** You're now ready to run all graph algorithms.
