"""
Additional layout functions for BIBAS graph visualizations.
Includes hierarchy-based, reversed, jittered, and radial layouts.
"""

import networkx as nx
from collections import defaultdict
import math
import random

def hierarchy_layout(G):
    depths = {}
    def compute_depth(node):
        if node in depths:
            return depths[node]
        children = list(G.successors(node))
        if not children:
            depth = 0
        else:
            depth = 1 + max(compute_depth(child) for child in children)
        depths[node] = depth
        return depth

    for node in G.nodes():
        compute_depth(node)

    layers = defaultdict(list)
    for node, depth in depths.items():
        layers[depth].append(node)

    pos = {}
    max_depth = max(depths.values())
    for depth, nodes in layers.items():
        n = len(nodes)
        for i, node in enumerate(sorted(nodes)):
            x = i - (n - 1) / 2
            y = -(max_depth - depth)
            pos[node] = (x, y)

    return pos

def reversed_hierarchy_layout(G):
    depths = {}
    def compute_depth(node):
        if node in depths:
            return depths[node]
        children = list(G.successors(node))
        if not children:
            depth = 0
        else:
            depth = 1 + max(compute_depth(child) for child in children)
        depths[node] = depth
        return depth

    for node in G.nodes():
        compute_depth(node)

    layers = defaultdict(list)
    for node, depth in depths.items():
        layers[depth].append(node)

    pos = {}
    max_depth = max(depths.values())
    for depth, nodes in layers.items():
        n = len(nodes)
        for i, node in enumerate(sorted(nodes)):
            x = i - (n - 1) / 2
            y = max_depth - depth
            pos[node] = (x, y)

    return pos

def hierarchy_layout_jittered(G, jitter_strength=0.4, seed=None):
    """
    Returns a hierarchical layout for a directed graph with a random horizontal
    shift applied per layer to reduce edge overlap.

    Parameters:
        G : networkx.DiGraph
            The directed graph to layout.
        jitter_strength : float, optional (default=0.4)
            Maximum horizontal shift (positive or negative) applied to each layer.
        seed : int or None
            Seed for reproducible jitter.

    Returns:
        pos : dict
            A dictionary mapping each node to an (x, y) position.
    """
    if seed is not None:
        random.seed(seed)

    depths = {}
    def compute_depth(node):
        if node in depths:
            return depths[node]
        children = list(G.successors(node))
        if not children:
            depth = 0
        else:
            depth = 1 + max(compute_depth(child) for child in children)
        depths[node] = depth
        return depth

    for node in G.nodes():
        compute_depth(node)

    layers = defaultdict(list)
    for node, depth in depths.items():
        layers[depth].append(node)

    pos = {}
    max_depth = max(depths.values())
    for depth, nodes in layers.items():
        n = len(nodes)
        jitter = random.uniform(-jitter_strength, jitter_strength)
        for i, node in enumerate(sorted(nodes)):
            x = i - (n - 1) / 2 + jitter
            y = -(max_depth - depth)
            pos[node] = (x, y)

    return pos

def radial_layout(G):
    layers = defaultdict(list)
    visited = set()

    def assign_layer(node, depth):
        if node in visited:
            return
        visited.add(node)
        layers[depth].append(node)
        for child in G.successors(node):
            assign_layer(child, depth + 1)

    roots = [n for n in G.nodes() if G.in_degree(n) == 0]
    for root in roots:
        assign_layer(root, 0)

    pos = {}
    for depth, nodes in layers.items():
        radius = (depth + 1)
        angle_step = 2 * math.pi / len(nodes)
        for i, node in enumerate(nodes):
            theta = i * angle_step
            x = radius * math.cos(theta)
            y = radius * math.sin(theta)
            pos[node] = (x, y)

    return pos
