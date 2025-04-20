import numpy as np
import pandas as pd
import seaborn as sns
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pgmpy.models import DiscreteBayesianNetwork
from bibas.inference_utils import compute_bibas_pairwise, rank_sources_for_target


def plot_binary_bibas_heatmap(model, operation="observe", filename=None):
    nodes = sorted(model.nodes())

    # Validate that all variables are binary
    for node in nodes:
        cpd = model.get_cpds(node)
        if cpd.variable_card != 2:
            raise ValueError(f"All nodes must be binary. Node '{node}' has {cpd.variable_card} states.")

    # Compute BIBAS matrix
    bibas_matrix = pd.DataFrame(index=nodes, columns=nodes)
    for src in nodes:
        for tgt in nodes:
            if src == tgt:
                bibas_matrix.loc[src, tgt] = np.nan
            else:
                score = compute_bibas_pairwise(model, src, tgt, target_positive_state=1, operation=operation)
                bibas_matrix.loc[src, tgt] = score
    bibas_matrix = bibas_matrix.astype(float)

    # Plot
    n = len(nodes)
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

    ax.set_title(f"BIBAS Factor (operation = '{operation}')", fontsize=14)
    ax.set_xlabel("Target Node")
    ax.set_ylabel("Source Node")
    plt.xticks(rotation=0)
    plt.yticks(rotation=0)
    plt.tight_layout()

    if filename:
        plt.savefig(filename, bbox_inches="tight", dpi=300)
    else:
        plt.show()


def plot_ranked_sources_for_target(model, target, target_positive_state=1, operation="observe", filename=None):
    df = rank_sources_for_target(model, target, target_positive_state, operation)

    plt.figure(figsize=(10, 0.5 * len(df)))
    sns.barplot(data=df, x="bibas_score", y="source", palette="Reds_r")

    plt.xlabel("BIBAS Score")
    plt.ylabel("Source Node")
    plt.title(f"BIBAS Ranking on Target: '{target}' (operation = '{operation}')")

    # Annotate bars
    for i, row in df.iterrows():
        plt.text(row.bibas_score + 0.5, i, f"{row.bibas_score:.1f}", va='center')

    plt.xlim(0, df["bibas_score"].max() * 1.1)
    plt.tight_layout()

    if filename:
        plt.savefig(filename, bbox_inches="tight", dpi=300)
    else:
        plt.show()


def plot_bn(model, layout=nx.spring_layout, type="none", target=None, operation="observe", filename=None):
    if not isinstance(model, DiscreteBayesianNetwork):
        raise ValueError("Input must be a pgmpy DiscreteBayesianNetwork.")

    nodes = sorted(model.nodes())
    edges = model.edges()
    G = nx.DiGraph(edges)
    pos = layout(G, seed=42)

    def is_binary(node):
        return model.get_cpds(node).variable_card == 2

    if type in ['edges', 'edges_and_impacts']:
        non_binary_nodes = [n for n in nodes if not is_binary(n)]
        if non_binary_nodes:
            raise ValueError(f"Edge-based visualization requires all nodes to be binary. Non-binary: {non_binary_nodes}")

    node_colors = {}
    edge_colors = {}
    node_labels = {n: n for n in nodes}

    if type == "none":
        node_colors = {n: "skyblue" for n in nodes}

    elif type == "blanket":
        if not target:
            raise ValueError("Target must be specified for type='blanket'")
        blanket = set(model.get_markov_blanket(target))
        for node in nodes:
            if node == target:
                node_colors[node] = "lightgreen"
            elif node in blanket:
                node_colors[node] = "salmon"
            else:
                node_colors[node] = "skyblue"

    elif type == "impacts":
        if not target:
            raise ValueError("Target must be specified for type='impacts'")
        bibas_scores = {
            node: compute_bibas_pairwise(model, node, target, operation=operation)
            if node != target else None
            for node in nodes
        }
        max_score = max(v for v in bibas_scores.values() if v is not None)
        for node in nodes:
            if node == target:
                node_colors[node] = "lightgreen"
            else:
                score = bibas_scores[node]
                color_intensity = score / max_score if score is not None else 0
                node_colors[node] = (1, 1 - color_intensity, 1 - color_intensity)
                node_labels[node] = f"{node}\n{score:.2f}"

    elif type == "edges":
        for (src, tgt) in edges:
            score = compute_bibas_pairwise(model, src, tgt, operation=operation)
            edge_colors[(src, tgt)] = (1, 1 - score/100, 1 - score/100)
        node_colors = {n: "skyblue" for n in nodes}

    elif type == "edges_and_impacts":
        if not target:
            raise ValueError("Target must be specified for type='edges_and_impacts'")
        bibas_scores = {
            node: compute_bibas_pairwise(model, node, target, operation=operation)
            if node != target else None
            for node in nodes
        }
        max_score = max(v for v in bibas_scores.values() if v is not None)
        for node in nodes:
            if node == target:
                node_colors[node] = "lightgreen"
            else:
                score = bibas_scores[node]
                color_intensity = score / max_score if score is not None else 0
                node_colors[node] = (1, 1 - color_intensity, 1 - color_intensity)
                node_labels[node] = f"{node}\n{score:.2f}"

        for (src, tgt) in edges:
            score = compute_bibas_pairwise(model, src, tgt, operation=operation)
            edge_colors[(src, tgt)] = (1, 1 - score/100, 1 - score/100)

    else:
        raise ValueError(f"Unknown type: '{type}'. Valid options: none, blanket, impacts, edges, edges_and_impacts.")

    fig, ax = plt.subplots(figsize=(1.2 * len(nodes), 1.2 * len(nodes)))

    nx.draw_networkx_nodes(G, pos, node_color=[node_colors[n] for n in nodes], node_size=1500, ax=ax)
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=10, ax=ax)

    if type in ["edges", "edges_and_impacts"]:
        edge_list = list(edge_colors.keys())
        edge_color_vals = list(edge_colors.values())
        nx.draw_networkx_edges(G, pos, edgelist=edge_list, edge_color=edge_color_vals, width=2, ax=ax)
    else:
        nx.draw_networkx_edges(G, pos, edge_color="gray", arrows=True, ax=ax)

    plt.title(f"BN Visualization ({type})", fontsize=14)
    plt.axis("off")

    if type == "blanket":
        import matplotlib.patches as mpatches
        legend_handles = [
            mpatches.Patch(color="lightgreen", label="Target"),
            mpatches.Patch(color="salmon", label="Markov Blanket"),
            mpatches.Patch(color="skyblue", label="Other Node")
        ]
        plt.legend(handles=legend_handles, loc='upper right', frameon=True)

    plt.tight_layout()

    if filename:
        plt.savefig(filename, bbox_inches="tight", dpi=300)
    else:
        plt.show()