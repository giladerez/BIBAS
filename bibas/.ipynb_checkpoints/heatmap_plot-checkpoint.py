import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from .inference_utils import compute_bibas_pairwise

def plot_bibas_heatmap(model, sort_nodes=True, hatch_diagonal=True):
    nodes = sorted(model.nodes()) if sort_nodes else list(model.nodes())
    bibas_matrix = pd.DataFrame(index=nodes, columns=nodes)

    for source in nodes:
        for target in nodes:
            if source == target:
                bibas_matrix.loc[source, target] = np.nan
            else:
                bibas_matrix.loc[source, target] = compute_bibas_pairwise(model, source, target)

    bibas_matrix = bibas_matrix.astype(float)

    plt.figure(figsize=(1 + len(nodes) * 0.6, 6))
    ax = sns.heatmap(
        bibas_matrix,
        annot=True,
        fmt=".1f",
        cmap='Reds',
        square=True,
        linewidths=0.5,
        linecolor='white',
        cbar_kws={"label": "BIBAS Score"},
        mask=np.eye(len(bibas_matrix), dtype=bool)
    )

    if hatch_diagonal:
        for i in range(len(bibas_matrix)):
            rect = patches.Rectangle((i, i), 1, 1, hatch='///',
                                     fill=False, edgecolor='gray', linewidth=0)
            ax.add_patch(rect)

    plt.title("BIBAS Factor: Impact from Source to Target", fontsize=14)
    plt.xlabel("Target Node")
    plt.ylabel("Source Node")
    plt.xticks(rotation=0)
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.show()