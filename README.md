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

## **compute_bibas_pairwise**

```python
compute_bibas_pairwise(model, source, target, *, target_positive_state=1, operation="observe")
```

Compute the BIBAS score from **source** to **target** in a discrete Bayesian network.


**Parameters**

- **model** : *pgmpy.models.DiscreteBayesianNetwork*
  A fully specified discrete BN that already passed `model.check_model()`.

- **source** : *str*
  Name of the source node.

- **target** : *str*
  Name of the target node. Must be binary (exactly two states).

- **target_positive_state** : *int | str*, *default* `1`
  State of the binary target considered *positive*. Either its index (0/1) or its state name.

- **operation** : *{'observe', 'do'}*, *default* `"observe"`
  `'observe'` uses conditional evidence, `'do'` uses an intervention (do‑calculus).


**Returns**

- *float* — BIBAS score scaled to 0 – 100. Returns `None` when the score is undefined.


**Raises**

- **ValueError** — If the target is non‑binary or *operation* is invalid.


**Examples**

```python
score = compute_bibas_pairwise(model, "X", "Y", operation="do")
```


---

## **rank_sources_for_target**

```python
rank_sources_for_target(model, target, *, target_positive_state=1, operation="observe")
```

Rank every node (except **target**) by its BIBAS impact on that target.


**Parameters**

- **model** : *pgmpy.models.DiscreteBayesianNetwork*
  The Bayesian network.

- **target** : *str*
  Binary target node.

- **target_positive_state** : *int*, *default* `1`
  Positive state index.

- **operation** : *{'observe', 'do'}*, *default* `"observe"`
  Influence definition, identical to *compute_bibas_pairwise*.


**Returns**

- *pandas.DataFrame* — Columns `source`, `bibas_score`, sorted descending.


**Raises**

- **ValueError** — If *target* is not binary.


---

## **plot_binary_bibas_heatmap**

```python
plot_binary_bibas_heatmap(model, *, operation="observe", filename=None, title=None)
```

Draw a heat‑map of pairwise BIBAS scores in an all‑binary Bayesian network.


**Parameters**

- **model** : *pgmpy.models.DiscreteBayesianNetwork*
  All nodes must be binary.

- **operation** : *{'observe', 'do'}*, *default* `"observe"`
  Influence definition.

- **filename** : *str | None*
  If provided, save the figure to this path. Otherwise display it.

- **title** : *str | None*
  Custom plot title.


**Raises**

- **ValueError** — If any node is non‑binary.


---

## **plot_ranked_sources_for_target**

```python
plot_ranked_sources_for_target(model, target, *, target_positive_state=1, operation="observe", filename=None, title=None)
```

Horizontal bar chart ranking sources by their BIBAS score on a binary target.


**Parameters**

- **model** : *pgmpy.models.DiscreteBayesianNetwork*
  The network.

- **target** : *str*
  Binary target node.

- **target_positive_state** : *int*, *default* `1`
  Positive state index.

- **operation** : *{'observe', 'do'}*, *default* `"observe"`
  Influence definition.

- **filename** : *str | None*
  Optional save path.

- **title** : *str | None*
  Optional plot title.


---

## **plot_bn**

```python
plot_bn(model, *, layout=nx.spring_layout, type="none", target=None, operation="observe", filename=None, title=None, layout_kwargs=None)
```

Visualise a Bayesian network with optional BIBAS‑based colouring.


**Parameters**

- **model** : *pgmpy.models.DiscreteBayesianNetwork*
  Network to draw.

- **layout** : *callable*, *default* `nx.spring_layout`
  Layout function (NetworkX or `bibas.extra_layouts`).

- **type** : *{"none", "blanket", "impacts", "edges", "edges_and_impacts"}*, *default* `"none"`
  Visual style.

- **target** : *str | None*
  Required when *type* uses blanket or impact information.

- **operation** : *{'observe', 'do'}*, *default* `"observe"`
  Influence definition for impact modes.

- **filename** : *str | None*
  File path to save the figure.

- **title** : *str | None*
  Plot title.

- **layout_kwargs** : *dict | None*
  Extra arguments passed to *layout*.


**Raises**

- **ValueError** — For invalid *type*, missing *target*, non‑binary edge modes, or non‑discrete model.


---

## **hierarchy_layout**

```python
hierarchy_layout(G)
```

Return a vertical hierarchy layout for a directed graph.


**Parameters**

- **G** : *networkx.DiGraph*
  Directed graph to layout.


**Returns**

- *dict* — Mapping of nodes to **(x, y)** coordinates.


---

## **reversed_hierarchy_layout**

```python
reversed_hierarchy_layout(G)
```

Same as *hierarchy_layout* but flipped vertically (roots at the bottom).


**Parameters**

- **G** : *networkx.DiGraph*
  Directed graph to layout.


**Returns**

- *dict* — Mapping of nodes to **(x, y)** coordinates.


---

## **hierarchy_layout_jittered**

```python
hierarchy_layout_jittered(G, *, jitter_strength=0.4, seed=None)
```

Hierarchy layout with random horizontal jitter to reduce edge overlap.


**Parameters**

- **G** : *networkx.DiGraph*
  Directed graph to layout.

- **jitter_strength** : *float*, *default* `0.4`
  Maximum horizontal shift per layer.

- **seed** : *int | None*
  Random seed for reproducible jitter.


**Returns**

- *dict* — Mapping of nodes to **(x, y)** coordinates.


---

## **radial_layout**

```python
radial_layout(G)
```

Place root nodes at the centre and children on concentric circles.


**Parameters**

- **G** : *networkx.DiGraph*
  Directed graph to layout.


**Returns**

- *dict* — Mapping of nodes to **(x, y)** coordinates.


---
