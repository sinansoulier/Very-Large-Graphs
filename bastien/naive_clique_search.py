import itertools

import networkx as nx
from tqdm import tqdm


def nodes_combinations(nodes: list, i: int):
    return itertools.combinations(nodes, i)


def is_clique(G, nodes):
    combinations = nodes_combinations(nodes, 2)
    for u, v in combinations:
        if v not in G.neighbors(u):
            return False
    return True


def naive_clique_search(G: nx.graph):
    max_clique = set()
    max_clique_size = 0

    for i in tqdm(range(1, G.number_of_nodes() + 1), desc="Naive clique search"):
        combinations = list(nodes_combinations(G.nodes(), i))
        for nodes in (combinations):
            nodes = list(nodes)
            if len(nodes) > max_clique_size and is_clique(G, nodes):
                max_clique = set(nodes)
                max_clique_size = len(max_clique)
    return max_clique
