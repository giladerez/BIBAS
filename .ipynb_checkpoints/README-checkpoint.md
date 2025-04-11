# BIBAS: Bayesian Network Impact Heatmap

BIBAS (Bayesian Networks Impact Factor Based on Analysis of Sensitivity) computes a pairwise sensitivity score between all nodes in a Bayesian Network and visualizes the result in a clean heatmap.

## Features
- Visualize how much any source variable affects a target variable's prediction certainty - upon observing the source value.
- Easy `.plot_bibas_heatmap(model)` interface
- Striped diagonal for self-impact exclusion
- Supports `pgmpy` models (DiscreteBayesianNetwork) with only binary nodes (for a code supporting more states, check out my thesis or contact me)

## Example

```python
from bibas.heatmap_plot import plot_bibas_heatmap
plot_bibas_heatmap(model)