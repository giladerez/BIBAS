import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patches as patches
from pgmpy.inference import VariableElimination

def compute_bibas_pairwise(model, source, target):
    infer = VariableElimination(model)
    try:
        p0 = infer.query(variables=[target], evidence={source: 0}).values[1]
        p1 = infer.query(variables=[target], evidence={source: 1}).values[1]
        return abs(p1 - p0) * 100
    except:
        return np.nan

def plot_bibas_heatmap(model):
    nodes = sorted(model.nodes())
    n = len(nodes)

    # Compute BIBAS matrix
    bibas_matrix = pd.DataFrame(index=nodes, columns=nodes)
    for src in nodes:
        for tgt in nodes:
            if src == tgt:
                bibas_matrix.loc[src, tgt] = np.nan
            else:
                bibas_matrix.loc[src, tgt] = compute_bibas_pairwise(model, src, tgt)
    bibas_matrix = bibas_matrix.astype(float)

    # Plot
    fig, ax = plt.subplots(figsize=(1.2 * n, 1.1 * n))
    sns.heatmap(
        bibas_matrix,
        annot=True,
        fmt=".1f",
        cmap='Reds',
        square=True,
        linewidths=0.5,
        linecolor='white',
        mask=np.eye(n, dtype=bool),
        cbar_kws={"label": "BIBAS Score", "shrink": 0.6},
        ax=ax
    )

    # Add hatched diagonal
    for i in range(n):
        rect = patches.Rectangle((i, i), 1, 1, hatch='///',
                                 fill=False, edgecolor='gray', linewidth=0)
        ax.add_patch(rect)

    ax.set_title("BIBAS Factor: Impact from Source to Target", fontsize=14)
    ax.set_xlabel("Target Node")
    ax.set_ylabel("Source Node")
    plt.xticks(rotation=0)
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.show()