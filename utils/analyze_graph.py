import numpy as np
import networkx as nx


def compute_misinformation_risk(G: nx.Graph) -> dict:
    """
    Returns the calculated risk score associated with each node in the provided graph.

    Args:
        G: The graph whose nodes are to be assessed for risk.
    """
    # PageRank
    pr = nx.pagerank(G)
    pr_vals = list(pr.values())
    pr_threshold = np.percentile(list(pr_vals), 90) # Top 10%

    # K-core
    core_nums = nx.core_number(G)
    max_core = max(core_nums.values())

    # Articulation Points
    articulation = set(nx.articulation_points(G))

    # Bridges (edge-level)
    bridges = set(nx.bridges(G))
    bridge_counts = {
        n: 0 for n in G.nodes()
    }
    for u, v in bridges:
        bridge_counts[u] += 1
        bridge_counts[v] += 1

    # Clustering
    clust_coef = nx.clustering(G)
    clust_vals = list(clust_coef.values())
    clust_threshold = np.percentile(clust_vals, 75) # Top 25%

    # Betweenness
    btw = nx.betweenness_centrality(G, k=min(200, G.number_of_nodes()))
    btw_threshold = np.percentile(list(btw.values()), 90)   # Top 10%

    risk_scores = {}

    # Tallies up risk for each node
    for n in G.nodes():
        score = 0

        # Echo chamber zone
        if clust_coef[n] >= clust_threshold:
            score += 1

        # Influential node
        if pr[n] >= pr_threshold:
            score += 2

        # Gatekeeper node
        if btw[n] >= btw_threshold:
            score += 2
        
        # Structural bottleneck
        if n in articulation:
            score += 2

        # Community-hopping nodes
        if bridge_counts[n] >= 3:
            score += 2
        elif bridge_counts[n] >= 1:
            score += 1

        # Super-spreader zone
        if core_nums[n] == max_core:
            score += 3
        
        risk_scores[n] = score

    return risk_scores

