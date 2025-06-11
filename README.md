# BIBAS: Bayesian-network Impact factor Based on Analysis of Shifts
Quantify node-to-node impact, rank influential sources, and visualise
Bayesian Networks with publication-quality layouts.

<p align="center">
  <img src="examples/asia_edges_and_impacts.png" width="500"/>
</p>

---

## What’s inside (v0.2.0)

| Area                      | Key objects (import paths)                                           |
|---------------------------|-----------------------------------------------------------------------|
| **Impact metrics**        | `bibas.inference_utils.compute_bibas_pairwise`  •  `rank_sources_for_target` |
| **Heatmaps & bar-plots**  | `bibas.visual_analysis.plot_binary_bibas_heatmap`  •  `plot_ranked_sources_for_target` |
| **Full BN visualisation** | `bibas.visual_analysis.plot_bn`  – 5 modes: *none · blanket · impacts · edges · edges_and_impacts* |
| **Custom graph layouts**  | `bibas.extra_layouts`  (hierarchy, reversed hierarchy, jittered, radial) |
| **observation & intervention** | All metrics work with `operation="observe"` **or** `operation="do"` |

---

## 📦 Installation
```bash
pip install bibas     # Python ≥ 3.7
```

---

## 🚀 Quick Start
```python
import networkx as nx
from pgmpy.utils import get_example_model
from bibas import (
    compute_bibas_pairwise,
    plot_binary_bibas_heatmap,
    plot_ranked_sources_for_target,
    plot_bn,
)

# 1 Load demo network
model  = get_example_model("asia")
target = "dysp"        # binary node

# 2 Pairwise impact heat‑map (observe)
plot_binary_bibas_heatmap(model, operation="observe")

# 3 Top sources influencing a target (intervention)
plot_ranked_sources_for_target(model, target, operation="do")

# 4 Structure plot with edge & node impacts
plot_bn(model,
        layout=nx.spring_layout,
        type="edges_and_impacts",
        target=target,
        operation="observe")
```

<p align="center">
  <img src="examples/asia_heatmap.png" width="650"/>
</p>

---

## 📐 Layout Gallery

| Layout helper                                   | Visual style (depth) | Typical use‑case                        |
|-------------------------------------------------|----------------------|-----------------------------------------|
| `hierarchy_layout`                              | Top‑down layers      | Highlight generational flow             |
| `reversed_hierarchy_layout`                     | Bottom‑up layers     | Trace effects backwards                 |
| `hierarchy_layout_jittered`                     | Top‑down + jitter    | Reduce edge crowding in wide layers     |
| `radial_layout`                                 | Concentric circles   | Show symmetry / centrality              |


```python
from bibas.extra_layouts import hierarchy_layout_jittered
plot_bn(model, layout=hierarchy_layout_jittered, layout_kwargs={"seed": 4, "jitter_strength": 0.4}, type="blanket", target="dysp")
```

---
## 📝 Functionalities (for examples see Example Notebook ahead)

| Function | Signature | Purpose |
|----------|-----------|---------|
| `compute_bibas_pairwise` | `compute_bibas_pairwise(model, operation='observe')` | Return a full node × node impact matrix (observe / do). |
| `rank_sources_for_target` | `rank_sources_for_target(model, target, operation='observe')` | Rank all source nodes by their influence on a binary *target* state. |
| `plot_binary_bibas_heatmap` | `plot_binary_bibas_heatmap(model, operation='observe', ax=None, **heatmap_kwargs)` | Draw an annotated heat-map of positive-state impacts. |
| `plot_ranked_sources_for_target` | `plot_ranked_sources_for_target(model, target, operation='observe', top_n=10, ax=None, **bar_kwargs)` | Horizontal bar-plot of the top–N influential sources for a target. |
| `plot_bn` | `plot_bn(model, layout='spring', type='blanket', target=None, operation='observe', ax=None, **layout_kwargs)` | Visualise the BN with optional blankets, impact colouring, or edge weights. |
| `hierarchy_layout` | `hierarchy_layout(G)` | Top-down layers based on depth (ideal for DAGs). |
| `reversed_hierarchy_layout` | `reversed_hierarchy_layout(G)` | Bottom-up view: deepest nodes appear at the top. |
| `hierarchy_layout_jittered` | `hierarchy_layout_jittered(G, jitter_strength=0.4, seed=None)` | Hierarchical layout with horizontal jitter to reduce edge overlap. |
| `radial_layout` | `radial_layout(G)` | Concentric rings by depth; emphasises symmetry and centrality. |

---

## Example Notebook  
See **`examples/asia_demo.ipynb`** for a fully reproducible walkthrough of every functionality in this README.


***

<br>
<br>
<br>

# BIBAS API reference

## compute_bibas_pairwise

<p style="font-family:SFMono-Regular,Consolas,Menlo,monospace;font-size:90%">
compute_bibas_pairwise(<strong>model</strong>, <strong>source</strong>, <strong>target</strong>, target_positive_state=1, operation="observe")
</p>

Compute the BIBAS influence score from a source node to a (binary) target.

### Parameters  
- **model** - `pgmpy.models.DiscreteBayesianNetwork`  
  The Bayesian network.  
- **source** - `str`  
  Name of the source variable.  
- **target** - `str`  
  Name of the binary target variable.  
- **target_positive_state** - `int | str`, default `1`  
  Which state of the target is considered “positive”.  
- **operation** - `{"observe", "do"}`, default `"observe"`  
  Whether to measure observational or interventional impact.

### Returns  
`float` - BIBAS score in the range 0-100.

### Example  
```python
from bibas.inference_utils import compute_bibas_pairwise
score = compute_bibas_pairwise(bn, "AGE", "DISEASE")
print(f"AGE → DISEASE BIBAS: {score:.2f}")
```

---

## rank_sources_for_target

<p style="font-family:SFMono-Regular,Consolas,Menlo,monospace;font-size:90%">
rank_sources_for_target(<strong>model</strong>, <strong>target</strong>, target_positive_state=1, operation="observe")
</p>

Rank every non-target node by its BIBAS impact on the given binary target.

### Parameters  
- **model** - `pgmpy.models.DiscreteBayesianNetwork`  
- **target** - `str`  
- **target_positive_state** - `int | str`, default `1`  
- **operation** - `{"observe", "do"}`, default `"observe"`

### Returns  
`pandas.DataFrame` with columns `source` and `bibas_score`, sorted descending.

### Example  
```python
from bibas.inference_utils import rank_sources_for_target
df = rank_sources_for_target(bn, "DISEASE")
print(df.head())
```

---

## plot_binary_bibas_heatmap

<p style="font-family:SFMono-Regular,Consolas,Menlo,monospace;font-size:90%">
plot_binary_bibas_heatmap(<strong>model</strong>, operation="observe", filename=None, title=None)
</p>

Draw a heat-map of pairwise BIBAS scores for a fully binary network.

### Parameters  
- **model** - `pgmpy.models.DiscreteBayesianNetwork`  
- **operation** - `{"observe", "do"}`, default `"observe"`  
- **filename** - `str | None`, default `None`  
  Path to save the figure instead of showing it.  
- **title** - `str | None`, default `None`

### Returns  
`None` - Displays or saves a figure.

### Example  
```python
from bibas.visual_analysis import plot_binary_bibas_heatmap
plot_binary_bibas_heatmap(bn, operation="do")
```

---

## plot_ranked_sources_for_target

<p style="font-family:SFMono-Regular,Consolas,Menlo,monospace;font-size:90%">
plot_ranked_sources_for_target(<strong>model</strong>, <strong>target</strong>, target_positive_state=1, operation="observe", filename=None, title=None)
</p>

Horizontal bar-chart of BIBAS scores toward one binary target.

### Parameters  
- **model** - `pgmpy.models.DiscreteBayesianNetwork`  
- **target** - `str`  
- **target_positive_state** - `int | str`, default `1`  
- **operation** - `{"observe", "do"}`, default `"observe"`  
- **filename** - `str | None`, default `None`  
- **title** - `str | None`, default `None`

### Returns  
`None`

### Example  
```python
from bibas.visual_analysis import plot_ranked_sources_for_target
plot_ranked_sources_for_target(bn, "DISEASE")
```

---

## plot_bn

<p style="font-family:SFMono-Regular,Consolas,Menlo,monospace;font-size:90%">
plot_bn(<strong>model</strong>, layout=nx.spring_layout, type="none", target=None, operation="observe", filename=None, title=None)
</p>

Versatile NetworkX-based visualisation of the Bayesian network with optional BIBAS overlays.

### Parameters  
- **model** - `pgmpy.models.DiscreteBayesianNetwork`  
- **layout** - `callable`, default `nx.spring_layout`  
- **type** - `{"none", "blanket", "impacts", "edges", "edges_and_impacts"}`, default `"none"`  
- **target** - `str | None`, default `None`  
- **operation** - `{"observe", "do"}`, default `"observe"`  
- **filename** - `str | None`, default `None`  
- **title** - `str | None`, default `None`

### Returns  
`None`

### Example  
```python
from bibas.visual_analysis import plot_bn
plot_bn(bn, type="blanket", target="DISEASE")
```

---

## hierarchy_layout

<p style="font-family:SFMono-Regular,Consolas,Menlo,monospace;font-size:90%">
hierarchy_layout(<strong>G</strong>)
</p>

Produce top-down coordinates for hierarchical drawing.

### Parameters  
- **G** - `networkx.DiGraph`

### Returns  
`dict` mapping node → (x, y) coordinates.

### Example  
```python
pos = hierarchy_layout(G)
```

---

## reversed_hierarchy_layout

<p style="font-family:SFMono-Regular,Consolas,Menlo,monospace;font-size:90%">
reversed_hierarchy_layout(<strong>G</strong>)
</p>

Bottom-up variant of `hierarchy_layout`.

### Parameters  
- **G** - `networkx.DiGraph`

### Returns  
`dict` of positions.

### Example  
```python
pos = reversed_hierarchy_layout(G)
```

---

## radial_layout

<p style="font-family:SFMono-Regular,Consolas,Menlo,monospace;font-size:90%">
radial_layout(<strong>G</strong>)
</p>

Arrange nodes in concentric circles by depth.

### Parameters  
- **G** - `networkx.DiGraph`

### Returns  
`dict` of node positions.

### Example  
```python
pos = radial_layout(G)
```
