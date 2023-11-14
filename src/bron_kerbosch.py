import networkx as nx


class BronKerbosch:
    """
    Bron-Kerbosch class containing algorithm for finding all maximal cliques in a graph.
    The different implementations of the algorithm are:
    - bron_kerbosch: basic implementation
    - bron_kerbosch_with_pivot: implementation with pivot

    """
    def __init__(self, G: nx.graph, graph_name: str = 'G'):
        """
        Initialize BronKerbosch class with a graph G.
        Args:
            G (nx.graph): graph
            graph_name (str): name of the graph. Defaults to 'G'.
        """
        self.G = G
        self.graph_name = graph_name
        self.cliques = []

        # Initialize R, P, X disjoint sets.
        self.R = set()
        self.P = set(G.nodes)
        self.X = set()

    def reset(self):
        """
        Reset R, P, X disjoint sets, and cliques list.
        """
        self.cliques = []
        self.R = set()
        self.P = set(self.G.nodes)
        self.X = set()

    def bron_kerbosch(self, R: set, P: set, X: set):
        """
        Basic implementation of Bron-Kerbosch algorithm.

        Args:
            R (set): set of vertices in the current clique
            P (set): set of vertices that are candidates to be added to R
            X (set): set of vertices that are not candidates to be added to R
        """
        if not P and not X:
            self.cliques.append(R.copy())
            return

        for v in list(P):
            neighbors_v = set([n for n in self.G.neighbors(v)])
            self.bron_kerbosch(
                R.union([v]),
                P.intersection(neighbors_v),
                X.intersection(neighbors_v),
            )

            P.remove(v)
            X.add(v)

    def bron_kerbosch_pivot(self, R: set, P: set, X: set):
        """
        Implementation of Bron-Kerbosch algorithm with pivot.

        Args:
            R (set): set of vertices in the current clique
            P (set): set of vertices that are candidates to be added to R
            X (set): set of vertices that are not candidates to be added to R
        """
        if not P and not X:
            self.cliques.append(R.copy())
            return

        u = list(P.union(X))[0]
        neighbors_u = set([n for n in self.G.neighbors(u)])
        for v in list(P.difference(neighbors_u)):
            neighbors_v = set([n for n in self.G.neighbors(v)])
            self.bron_kerbosch_pivot(
                R.union([v]),
                P.intersection(neighbors_v),
                X.intersection(neighbors_v),
            )

            P.remove(v)
            X.add(v)

    def bron_kerbosch_degeneracy(self):
        """
        Implementation of Bron-Kerbosch algorithm with degeneracy ordering.
        """
        self.reset()
        # FIXME
        raise NotImplementedError
