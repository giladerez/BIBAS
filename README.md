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

---

## Inference Utilities

### compute_bibas_pairwise

<pre style="font-family: monospace; font-size: 15px;">compute_bibas_pairwise(<b>model</b>, <b>source</b>, <b>target</b>, <b>target_positive_state</b>=1, <b>operation</b>="observe")</pre>

Compute the BIBAS score from **source** to **target**.  
The target node must be binary.

**Parameters**

- **model** : `pgmpy.models.DiscreteBayesianNetwork` – A fitted Bayesian Network.  
- **source** : `str` – Name of the source node.  
- **target** : `str` – Name of the binary target node.  
- **target_positive_state** : `int | str`, default `1` – Which state of the target is considered positive.  
- **operation** : `{"observe","do"}`, default `"observe"` –  
  `"observe"` computes the associative impact, `"do"` computes the causal impact.

**Returns**

- `float` – BIBAS score in the range 0‑100, or `None` if computation fails.

**Example**

```python
from bibas.inference_utils import compute_bibas_pairwise
score = compute_bibas_pairwise(model, "AGE", "DISEASE")
print(f"BIBAS AGE → DISEASE = {score:.2f}")
```

---

### rank_sources_for_target

<pre style="font-family: monospace; font-size: 15px;">rank_sources_for_target(<b>model</b>, <b>target</b>, <b>target_positive_state</b>=1, <b>operation</b>="observe")</pre>

Rank every node (except the **target**) by its BIBAS impact on that target.

**Parameters**

- **model** : `pgmpy.models.DiscreteBayesianNetwork` – A fitted Bayesian Network.  
- **target** : `str` – Binary target node.  
- **target_positive_state** : `int | str`, default `1` – Which state of the target is considered positive.  
- **operation** : `{"observe","do"}`, default `"observe"` – Impact type to compute.

**Returns**

- `pandas.DataFrame` with columns `["source","bibas_score"]`, sorted descending.

**Example**

```python
from bibas.inference_utils import rank_sources_for_target
df = rank_sources_for_target(model,
                            target="DISEASE"
                            target_positive_state="yes",
                            operation="observe")
df.head()
```

---

## Visual Analysis

### plot_binary_bibas_heatmap

<pre style="font-family: monospace; font-size: 15px;">plot_binary_bibas_heatmap(<b>model</b>, <b>operation</b>="observe", <b>filename</b>=None, <b>title</b>=None)</pre>

Plot a heatmap of the BIBAS score from every source to every target in a fully binary network.

**Parameters**

- **model** : `pgmpy.models.DiscreteBayesianNetwork` – A network with only binary nodes.  
- **operation** : `{"observe","do"}`, default `"observe"` – Impact type.  
- **filename** : `str | None`, default `None` – If given, save the plot to this file.  
- **title** : `str | None`, default `None` – Custom plot title.

**Returns**

- `None`

**Example**

```python
from bibas.visual_analysis import plot_binary_bibas_heatmap
plot_binary_bibas_heatmap(model,
                          operation="do",
                          title="My Network: BIBAS heat-map (do)")
```

---

### plot_ranked_sources_for_target

<pre style="font-family: monospace; font-size: 15px;">plot_ranked_sources_for_target(<b>model</b>, <b>target</b>, <b>target_positive_state</b>=1, <b>operation</b>="observe", <b>filename</b>=None, <b>title</b>=None)</pre>

Plot a horizontal bar chart ranking all sources by their BIBAS impact on a given binary **target**.

**Parameters**

- **model** : `pgmpy.models.DiscreteBayesianNetwork` – The network to analyse.  
- **target** : `str` – Binary target node.  
- **target_positive_state** : `int`, default `1` – Positive state index.  
- **operation** : `{"observe","do"}`, default `"observe"` – Impact type.  
- **filename** : `str | None`, default `None` – Optional save path.  
- **title** : `str | None`, default `None` – Optional plot title.

**Returns**

- `None`

**Example**

```python
from bibas.visual_analysis import plot_ranked_sources_for_target
plot_ranked_sources_for_target(model,
                              target="DISEASE",  
                              target_positive_state="Yes",
                              operation="observe",
                              title="BIBAS (observe) scores for disease")
```
---

### plot_bn

<pre style="font-family: monospace; font-size: 15px;">plot_bn(<b>model</b>, <b>layout</b>=nx.spring_layout, <b>type</b>="none", <b>target</b>=None, <b>operation</b>="observe", <b>filename</b>=None, <b>title</b>=None, <b>layout_kwargs</b>=None)</pre>

Visualise a Bayesian Network with optional BIBAS‑based node or edge colouring.

**Parameters**

- **model** : `pgmpy.models.DiscreteBayesianNetwork` – The network to plot.  
- **layout** : `function`, default `nx.spring_layout` – NetworkX layout function.  
- **type** : `str`, default `"none"` – One of `"none"`, `"blanket"`, `"impacts"`, `"edges"`, `"edges_and_impacts"`.  
- **target** : `str | None`, default `None` – Target node when required by **type**.  
- **operation** : `{"observe","do"}`, default `"observe"` – Impact type.  
- **filename** : `str | None`, default `None` – Optional save path.  
- **title** : `str | None`, default `None` – Optional plot title.  
- **layout_kwargs** : `dict | None`, default `None` – Extra kwargs passed to the layout.

**Returns**

- `None`

**Example**

```python
from bibas.visual_analysis import plot_bn
plot_bn(model, 
        layout=hierarchy_layout_jittered, 
        layout_kwargs={"seed": 42, "jitter_strength": 0.4},
        type="edges_and_impacts", 
        target = target,
        title = "Hierarchy Layout Jittered")
```

---

## Extra Layouts

### hierarchy_layout

<pre style="font-family: monospace; font-size: 15px;">hierarchy_layout(<b>G</b>)</pre>

Return a top‑down hierarchical layout for a directed graph.

**Parameters**

- **G** : `networkx.DiGraph` – Graph to layout.

**Returns**

- `dict` mapping node to `(x,y)` position.

**Example**

```python
from bibas.extra_layouts import hierarchy_layout
pos = hierarchy_layout(G)
```

---

### reversed_hierarchy_layout

<pre style="font-family: monospace; font-size: 15px;">reversed_hierarchy_layout(<b>G</b>)</pre>

Return a bottom‑up hierarchical layout for a directed graph.

**Parameters**

- **G** : `networkx.DiGraph`

**Returns**

- `dict` mapping node to `(x,y)` position.

**Example**

```python
from bibas.extra_layouts import reversed_hierarchy_layout
pos = reversed_hierarchy_layout(G)
```
---


### hierarchy_layout_jittered

<pre style="font-family: monospace; font-size: 15px;">hierarchy_layout_jittered(<b>G</b>, <b>jitter_strength</b>=0.4, <b>seed</b>=None)</pre>

Hierarchical layout with a small random horizontal shift applied per layer.

**Parameters**

- **G** : `networkx.DiGraph`  
- **jitter_strength** : `float`, default `0.4` – Maximum horizontal jitter.  
- **seed** : `int | None`, default `None` – Random seed.

**Returns**

- `dict` node‑position mapping.

**Example**

```python
from bibas.extra_layouts import hierarchy_layout_jittered
pos = hierarchy_layout_jittered(G,
                                seed=42,
                                jitter_strength=0.4)
```

---

### radial_layout

<pre style="font-family: monospace; font-size: 15px;">radial_layout(<b>G</b>)</pre>

Place nodes on concentric circles according to their depth from root.

**Parameters**

- **G** : `networkx.DiGraph`

**Returns**

- `dict` mapping node to `(x,y)`.

**Example**

```python
from bibas.extra_layouts import radial_layout
pos = radial_layout(G)
```
