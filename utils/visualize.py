import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches


def assign_colors(G: nx.Graph, page_type: dict) -> tuple:
    """
    Assigns a distinct color to each page type in the graph.

    Args:
        G: The graph whose nodes will be assigned colors.
        page_type: A mapping of node_id to category string representing each node's type.
    """
    unique_types = list(set(page_type.values()))
    color_map = {}

    # Pick distinct colors
    palette = list(mcolors.TABLEAU_COLORS.values())

    while len(palette) < len(unique_types):
        palette += palette  # repeat if needed

    type_to_color = {
        t: palette[i]
        for i, t
        in enumerate(unique_types)
    }

    for node in G.nodes():
        if node in page_type:
            color_map[node] = type_to_color[page_type[node]]
        else:
            color_map[node] = "#cccccc"  # default for missing labels
            
    return color_map, type_to_color


def sample_by_pagerank(pr: dict, k: int) -> list:
    """
    Selects the top-k nodes ranked by PageRank score.

    Args:
        pr: A dictionary mapping node_id → PageRank score.
        k: The number of highest-ranked nodes to return.
    """
    ranked = sorted(pr, key=pr.get, reverse=True)
    return ranked[:k]


def sample_by_page_type(G: nx.Graph, page_type: dict, pr: int, k_per_type: int=100):
    """
    Samples nodes by category, selecting the top-ranked nodes within each page type according to PageRank.
    
    Args:
        G: The full graph containing all nodes.
        page_type: A mapping of node_id to category string.
        pr: A dictionary mapping node_id to PageRank score.
        k_per_type: Number of nodes to sample from each page type.
    """
    sampled = []
    nodes_by_type = {}

    # 
    for node in G.nodes():
        if node in page_type:
            t = page_type[node]
            nodes_by_type.setdefault(t, []).append(node)

    # 
    for t, nodes in nodes_by_type.items():
        ranked = sorted(nodes, key=lambda n: pr[n], reverse=True)
        sampled.extend(ranked[:k_per_type])

    return sampled


def visualize_colored_sample(G: nx.Graph, sampled_nodes: list, color_map: list, type_to_color: dict, title: str):
    """
    Visualizes a sampled subgraph using category-based color coding.
    
    Args:
        G: The graph from which a subgraph will be generated from.
        sampled_nodes: IDs of nodes that are to be plotted.
        color_map: A mapping of node_id to color representing each node’s assigned color.
        type_to_color: A mapping of page_type to color used to build the legend.
        title: The title of the plot figure.
    """
    H = G.subgraph(sampled_nodes).copy()

    pos = nx.spring_layout(H, k=1, iterations=50)

    plt.title(title)

    # Create proxy artists for legend
    legend_handles = [
        mpatches.Patch(color=color, label=ptype)
        for ptype, color in type_to_color.items()
    ]

    plt.legend(
        handles=legend_handles,
        loc='lower right',
        title="Page Types",
        frameon=True,
        fontsize=8
    )

    nx.draw(
        H,
        pos,
        node_color=[color_map[n] for n in H.nodes()],
        node_size=40,
        width=0.3,
        with_labels=False
    )
    plt.show()


def visualize_sample(G: nx.Graph, sampled_nodes: list, color: str, title: str):
    """
    Displays graph for single community.
    
    Args:
        G: The graph from which a subgraph will be generated from.
        sampled_nodes: The obtained nodes that are to be plotted.
        color: The color of the nodes.
        title: The title of the plot figure.
    """
    plt.title(title)
    H = G.subgraph(sampled_nodes).copy()
    pos = nx.spring_layout(H, k=0.95, iterations=100)
    nx.draw(
        H,
        pos,
        node_size=40,
        node_color=color,
        width=0.3,
        with_labels=False
    )
    plt.show()


def visualize_graph(G: nx.Graph, title: str, sample_size: int, color_code: bool=False, color: str=None) -> None:
    """
    Displays the graph 

    Args:
        G: The graph from which a subgraph will be generated from.
        sample_size: The number of nodes to plot.
        color_code: Flag indicating if multiple communities are to be plotted and given unique colors.
        color: The uniform color all nodes will take on.
    """

    page_type = None

    # Load page_type metadata
    if color_code:
        targets = pd.read_csv("data/facebook_large/musae_facebook_target.csv")
        page_type = dict(zip(targets["id"], targets["page_type"]))

    # Compute PageRank
    pr = nx.pagerank(G)

    # Visualize multiple communities
    if color_code and page_type:
        # Divy up total number of nodes to display between communities
        if sample_size:
            k_per_type = int(sample_size / 4)
        else:
            k_per_type = 100

        # Sample nodes per category
        sampled_nodes = sample_by_page_type(G, page_type, pr, k_per_type)

        color_map, type_to_color = assign_colors(G, page_type)
        visualize_colored_sample(G, sampled_nodes, color_map, type_to_color, title)
    # Visualize a single community
    else:
        # Generic PageRank sampling (no categories)
        sampled_nodes = sample_by_pagerank(pr, k=sample_size)
        visualize_sample(G, sampled_nodes, color, title)
