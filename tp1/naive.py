import networkx as nx
import itertools

def recherche_naive_clique(G):
    """
    Trouve la plus grande clique dans le graphe G.
    """
    n = G.number_of_nodes()
    taille_max_clique = 0
    clique_max = set()

    # Parcourir tous les sous-ensembles de sommets de G
    for i in range(1, n + 1):
        for S in itertools.combinations(G.nodes(), i):
            if len(S) > taille_max_clique and est_clique(G, S):
                taille_max_clique = len(S)
                clique_max = set(S)

    return clique_max

def est_clique(G, S):
    """
    Vérifie si un ensemble de sommets S forme un clique dans le graphe G.
    """
    for u, v in itertools.combinations(S, 2):
        if G.has_edge(u, v) == False:
            return False
    return True

