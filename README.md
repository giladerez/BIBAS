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

## Function references

<!-- GLOBAL STYLES -->
<style scoped>
.bibas-doc              { font-family: "Helvetica Neue", Arial, sans-serif; color:#222; line-height:1.55; }
.bibas-doc h1           { font-size:1.9rem; margin:1.5em 0 0.5em; }
.bibas-doc h2           { font-size:1.4rem; margin:1.3em 0 0.4em; border-bottom:1px solid #e1e4e5; }
.bibas-doc h3           { font-size:1.15rem; margin:1.1em 0 0.3em; }
.bibas-doc code, .sig   { font-family:SFMono-Regular, Consolas, "Liberation Mono", monospace; color:#c92c2c; }
.bibas-doc dl           { margin:0 0 1.2em 0; }
.bibas-doc dt           { margin:0.3em 0 0; font-weight:600; }
.bibas-doc dd           { margin:0 0 0.6em 1.6em; }
.param-name             { color:#005cc5; }
.return-type            { color:#0969da; }
.exc-name               { color:#d73a49; }
</style>

<div class="bibas-doc">


# **bibas.inference_utils**

## **compute_bibas_pairwise**
<span class="sig">compute_bibas_pairwise(model, source, target, target_positive_state=1, operation="observe")</span>  
Compute the BIBAS score from *source* to *target* in a discrete Bayesian network.

### **Parameters**
<dl>
  <dt><span class="param-name">model</span> : <span class="return-type">pgmpy.models.DiscreteBayesianNetwork</span></dt>
  <dd>A fully specified and validated discrete BN (<code>model.check_model()</code> already called).</dd>

  <dt><span class="param-name">source</span> : <span class="return-type">str</span></dt>
  <dd>Name of the source node.</dd>

  <dt><span class="param-name">target</span> : <span class="return-type">str</span></dt>
  <dd>Name of the target node - must be binary (exactly two states).</dd>

  <dt><span class="param-name">target_positive_state</span> : <span class="return-type">int | str</span>, default 1</dt>
  <dd>Which state of the binary target is considered "positive", by index (0 or 1) or by state-name.</dd>

  <dt><span class="param-name">operation</span> : {<code>"observe"</code>, <code>"do"</code>}, default <code>"observe"</code></dt>
  <dd>
    • <code>"observe"</code> - influence via conditional evidence.<br>
    • <code>"do"</code> - influence under an intervention (do calculus).
  </dd>
</dl>

### **Returns**
<dl>
  <dt><span class="return-type">float</span></dt>
  <dd>BIBAS score between 0 and 100. Returns <code>None</code> when undefined.</dd>
</dl>

### **Raises**
<dl>
  <dt><span class="exc-name">ValueError</span></dt>
  <dd>If the target is non binary or <code>operation</code> is invalid.</dd>
</dl>

### **Example**
```python
score = compute_bibas_pairwise(model, "X", "Y", operation="do")
```

---

## **rank_sources_for_target**
<span class="sig">rank_sources_for_target(model, target, target_positive_state=1, operation="observe")</span>  
Rank all non target nodes by their BIBAS score on *target*.

### **Parameters**
<dl>
  <dt><span class="param-name">model</span> : <span class="return-type">DiscreteBayesianNetwork</span></dt>
  <dd>The Bayesian network.</dd>

  <dt><span class="param-name">target</span> : <span class="return-type">str</span></dt>
  <dd>Binary target node.</dd>

  <dt><span class="param-name">target_positive_state</span> : <span class="return-type">int</span>, default 1</dt>
  <dd>Positive state index.</dd>

  <dt><span class="param-name">operation</span> : {<code>"observe"</code>, <code>"do"</code>}, default <code>"observe"</code></dt>
  <dd>Same semantics as in <code>compute_bibas_pairwise</code>.</dd>
</dl>

### **Returns**
<dl>
  <dt><span class="return-type">pandas.DataFrame</span></dt>
  <dd>Columns: <code>source</code>, <code>bibas_score</code>, sorted descending.</dd>
</dl>

### **Raises**
<dl>
  <dt><span class="exc-name">ValueError</span></dt>
  <dd>If <code>target</code> is non binary.</dd>
</dl>


# **bibas.visual_analysis**

## **plot_binary_bibas_heatmap**
<span class="sig">plot_binary_bibas_heatmap(model, operation="observe", filename=None, title=None)</span>  
Draw a heatmap of pairwise BIBAS scores in an all binary network.

### **Parameters**
<dl>
  <dt><span class="param-name">model</span> : <span class="return-type">DiscreteBayesianNetwork</span></dt>
  <dd>All nodes must be binary.</dd>

  <dt><span class="param-name">operation</span> : {<code>"observe"</code>, <code>"do"</code>}, default <code>"observe"</code></dt>
  <dd>Influence definition.</dd>

  <dt><span class="param-name">filename</span> : <span class="return-type">str | None</span>, default <code>None</code></dt>
  <dd>Save path for a PNG file. If <code>None</code>, the plot is displayed.</dd>

  <dt><span class="param-name">title</span> : <span class="return-type">str | None</span>, default <code>None</code></dt>
  <dd>Custom plot title.</dd>
</dl>

### **Raises**
<dl>
  <dt><span class="exc-name">ValueError</span></dt>
  <dd>If any node is non binary.</dd>
</dl>

---

## **plot_ranked_sources_for_target**
<span class="sig">plot_ranked_sources_for_target(model, target, target_positive_state=1, operation="observe", filename=None, title=None)</span>  
Horizontal bar chart of BIBAS scores from each source to a binary target.

### **Parameters**
<dl>
  <dt><span class="param-name">model</span> : <span class="return-type">DiscreteBayesianNetwork</span></dt>
  <dd>The network.</dd>

  <dt><span class="param-name">target</span> : <span class="return-type">str</span></dt>
  <dd>Binary target node.</dd>

  <dt><span class="param-name">target_positive_state</span> : <span class="return-type">int</span>, default 1</dt>
  <dd>Positive state index.</dd>

  <dt><span class="param-name">operation</span> : {<code>"observe"</code>, <code>"do"</code>}, default <code>"observe"</code></dt>
  <dd>Influence definition.</dd>

  <dt><span class="param-name">filename</span> : <span class="return-type">str | None</span>, default <code>None</code></dt>
  <dd>Optional save path.</dd>

  <dt><span class="param-name">title</span> : <span class="return-type">str | None</span>, default <code>None</code></dt>
  <dd>Custom title.</dd>
</dl>

---

## **plot_bn**
<span class="sig">plot_bn(model, layout=nx.spring_layout, type="none", target=None, operation="observe", filename=None, title=None, layout_kwargs=None)</span>  
General BN visualisation with optional BIBAS based colouring.

### **Parameters**
<dl>
  <dt><span class="param-name">model</span> : <span class="return-type">DiscreteBayesianNetwork</span></dt>
  <dd>Network to draw.</dd>

  <dt><span class="param-name">layout</span> : <span class="return-type">callable</span>, default <code>nx.spring_layout</code></dt>
  <dd>Layout function (NetworkX or <code>bibas.extra_layouts</code>).</dd>

  <dt><span class="param-name">type</span> : <code>"none"</code> | <code>"blanket"</code> | <code>"impacts"</code> | <code>"edges"</code> | <code>"edges_and_impacts"</code>, default <code>"none"</code></dt>
  <dd>Visual style.</dd>

  <dt><span class="param-name">target</span> : <span class="return-type">str | None</span>, default <code>None</code></dt>
  <dd>Required for blanket / impact styles.</dd>

  <dt><span class="param-name">operation</span> : {<code>"observe"</code>, <code>"do"</code>}, default <code>"observe"</code></dt>
  <dd>Influence definition for impact modes.</dd>

  <dt><span class="param-name">filename</span> : <span class="return-type">str | None</span>, default <code>None</code></dt>
  <dd>Save path for the figure.</dd>

  <dt><span class="param-name">title</span> : <span class="return-type">str | None</span>, default <code>None</code></dt>
  <dd>Plot title.</dd>

  <dt><span class="param-name">layout_kwargs</span> : <span class="return-type">dict | None</span>, default <code>None</code></dt>
  <dd>Extra parameters passed to <code>layout</code>.</dd>
</dl>

### **Raises**
<dl>
  <dt><span class="exc-name">ValueError</span></dt>
  <dd>Invalid <code>type</code>, missing <code>target</code>, non binary nodes in edge modes, or if <code>model</code> is not discrete.</dd>
</dl>


# **bibas.extra_layouts**

## **hierarchy_layout**
<span class="sig">hierarchy_layout(G)</span>  
Vertical hierarchy layout by node depth.

## **reversed_hierarchy_layout**
<span class="sig">reversed_hierarchy_layout(G)</span>  
Same as <em>hierarchy_layout</em>, flipped vertically.

## **hierarchy_layout_jittered**
<span class="sig">hierarchy_layout_jittered(G, jitter_strength=0.4, seed=None)</span>  
Hierarchy layout with random horizontal jitter (reduces overlapping edges).

## **radial_layout**
<span class="sig">radial_layout(G)</span>  
Concentric circle layout with roots in the centre.


</div>

