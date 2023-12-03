import networkx as nx

from src.bron_kerbosch_pivot import bron_kerbosch_pivot_rec


def degeneracy_ordering(graph: nx.Graph):
    degeneracy_list = []
    degrees = {node: deg for _, (node, deg) in enumerate(graph.degree)}
    D = [[] for _ in range(max(degrees.values()) + 1)]

    for v, deg in zip(graph.nodes(), degrees.values()):
        D[deg].append(v)
    best_index = 0
    for _ in range(graph.number_of_nodes()):
        j = 0

        while not D[j]:
            j += 1
        best_index = max(best_index, j)
        v = D[j].pop(0)

        degeneracy_list.insert(0, v)

        for neighbor in graph.neighbors(v):
            if neighbor in degeneracy_list:
                continue
            assert (
                neighbor in D[degrees[neighbor]]
            ), f"""Vertex {neighbor} with degree {degrees[neighbor]} not in {D[degrees[neighbor]]}"""
            D[degrees[neighbor]].remove(neighbor)
            degrees[neighbor] = degrees[neighbor] - 1
            D[degrees[neighbor]].append(neighbor)

    return degeneracy_list


def bron_kerbosch_degeneracy(graph: nx.Graph, R: list = [], P: list = [], X: list = []):
    P = list(graph.nodes())
    clique = []
    max_clique = []
    deg = degeneracy_ordering(graph)
    for v in deg:
        neighbors = set(graph.neighbors(v))
        if v in neighbors:
            continue
        clique = bron_kerbosch_pivot_rec(
            graph,
            R + [v],
            P=[c for c in P if c in neighbors],
            X=[c for c in X if c in neighbors],
        )
        if len(clique) > len(max_clique):
            max_clique = clique
        P.remove(v)
        X.append(v)
    return max_clique
