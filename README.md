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

# BIBAS API Reference

This document provides concise reference information for the public functions exposed by **BIBAS**.  
The layout and typography mimic the style of the pandas API reference page.

---

## Module: `bibas.extra_layouts`

### `bibas.extra_layouts.hierarchy_layout`

<pre><code>bibas.extra_layouts.hierarchy_layout(<strong>G</strong>)</code></pre>

Compute a top‑down hierarchical position for every node in a directed graph.

**Parameters**

- **G** : `networkx.DiGraph`  
  Directed graph to lay out.

**Returns**

- `dict` – mapping each node to an `(x, y)` coordinate.

**Example**

```python
from bibas.extra_layouts import hierarchy_layout
pos = hierarchy_layout(G)
nx.draw(G, pos)
```

---

### `bibas.extra_layouts.reversed_hierarchy_layout`

<pre><code>bibas.extra_layouts.reversed_hierarchy_layout(<strong>G</strong>)</code></pre>

Compute a bottom‑up hierarchical layout (roots at the bottom).

**Parameters**

- **G** : `networkx.DiGraph`

**Returns**

- `dict` – positions keyed by node.

**Example**

```python
pos = reversed_hierarchy_layout(G)
```

---

### `bibas.extra_layouts.hierarchy_layout_jittered`

<pre><code>bibas.extra_layouts.hierarchy_layout_jittered(<strong>G</strong>, <strong>jitter_strength</strong>=0.4, <strong>seed</strong>=None)</code></pre>

Hierarchical layout with a small random horizontal jitter per layer to reduce edge overlap.

**Parameters**

- **G** : `networkx.DiGraph`
- **jitter_strength** : `float`, default `0.4`  
  Maximum horizontal offset applied in either direction.
- **seed** : `int or None`, default `None`  
  Random seed for reproducible jitter.

**Returns**

- `dict` – node positions.

**Example**

```python
pos = hierarchy_layout_jittered(G, jitter_strength=0.2, seed=42)
```

---

### `bibas.extra_layouts.radial_layout`

<pre><code>bibas.extra_layouts.radial_layout(<strong>G</strong>)</code></pre>

Arrange nodes on concentric circles around their root parents.

**Parameters**

- **G** : `networkx.DiGraph`

**Returns**

- `dict` – mapping of node to position.

**Example**

```python
pos = radial_layout(G)
```

---

## Module: `bibas.inference_utils`

### `bibas.inference_utils.compute_bibas_pairwise`

<pre><code>bibas.inference_utils.compute_bibas_pairwise(<strong>model</strong>, <strong>source</strong>, <strong>target</strong>, target_positive_state=1, operation="observe")</code></pre>

Compute the **BIBAS** impact score (0‑100) flowing from one variable to another.

**Parameters**

- **model** : `pgmpy.models.DiscreteBayesianNetwork`  
  Bayesian network.
- **source** : `str`  
  Source node name.
- **target** : `str`  
  Binary target node name.
- **target_positive_state** : `int or str`, default `1`  
  Which state of the target counts as positive.
- **operation** : `{"observe", "do"}`, default `"observe"`  
  Observation‑based or intervention‑based evaluation.

**Returns**

- `float` – BIBAS score in the range 0‑100, or `None` if not computable.

**Example**

```python
score = compute_bibas_pairwise(model, "AGE", "DISEASE")
```

---

### `bibas.inference_utils.rank_sources_for_target`

<pre><code>bibas.inference_utils.rank_sources_for_target(<strong>model</strong>, <strong>target</strong>, target_positive_state=1, operation="observe")</code></pre>

Rank every non‑target node by its BIBAS influence on a chosen binary target.

**Parameters**

- **model** : `pgmpy.models.DiscreteBayesianNetwork`
- **target** : `str`
- **target_positive_state** : `int or str`, default `1`
- **operation** : `{"observe", "do"}`, default `"observe"`

**Returns**

- `pandas.DataFrame` – two columns: `source` and `bibas_score`, sorted descending.

**Example**

```python
df_rank = rank_sources_for_target(model, "DISEASE")
df_rank.head()
```

---

## Module: `bibas.visual_analysis`

### `bibas.visual_analysis.plot_binary_bibas_heatmap`

<pre><code>bibas.visual_analysis.plot_binary_bibas_heatmap(<strong>model</strong>, operation="observe", filename=None, title=None)</code></pre>

Display (or save) a heatmap visualizing pairwise BIBAS scores across an all‑binary network.

**Parameters**

- **model** : `pgmpy.models.DiscreteBayesianNetwork`
- **operation** : `{"observe", "do"}`, default `"observe"`
- **filename** : `str or None`, default `None`  
  Path to write PNG file instead of showing interactively.
- **title** : `str or None`, default `None`

**Returns**

- `None`

**Example**

```python
plot_binary_bibas_heatmap(model, operation="do", filename="heatmap.png")
```

---

### `bibas.visual_analysis.plot_ranked_sources_for_target`

<pre><code>bibas.visual_analysis.plot_ranked_sources_for_target(<strong>model</strong>, <strong>target</strong>, target_positive_state=1, operation="observe", filename=None, title=None)</code></pre>

Horizontal bar chart of BIBAS scores for every source relative to a binary target.

**Parameters**

- **model** : `pgmpy.models.DiscreteBayesianNetwork`
- **target** : `str`
- **target_positive_state** : `int or str`, default `1`
- **operation** : `{"observe", "do"}`, default `"observe"`
- **filename** : `str or None`, default `None`
- **title** : `str or None`, default `None`

**Returns**

- `None`

**Example**

```python
plot_ranked_sources_for_target(model, "DISEASE")
```

---

### `bibas.visual_analysis.plot_bn`

<pre><code>bibas.visual_analysis.plot_bn(<strong>model</strong>, layout=nx.spring_layout, type="none", target=None, operation="observe", filename=None, title=None, layout_kwargs=None)</code></pre>

Versatile network plot with optional BIBAS‑based node coloring, edge coloring, and Markov blanket highlighting.

**Parameters**

- **model** : `pgmpy.models.DiscreteBayesianNetwork`
- **layout** : `callable`, default `nx.spring_layout`  
  Any NetworkX layout or a custom layout function.
- **type** : `str`, default `"none"`  
  One of `"none"`, `"blanket"`, `"impacts"`, `"edges"`, `"edges_and_impacts"`.
- **target** : `str or None`, default `None`  
  Required for blanket or impact visualizations.
- **operation** : `{"observe", "do"}`, default `"observe"`
- **filename** : `str or None`, default `None`
- **title** : `str or None`, default `None`
- **layout_kwargs** : `dict or None`, default `None`  
  Extra arguments passed to the chosen layout.

**Returns**

- `None`

**Example**

```python
plot_bn(model, type="impacts", target="DISEASE")
```

---

