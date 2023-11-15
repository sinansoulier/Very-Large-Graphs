import networkx as nx


class BronKerbosch:
    """
    Bron-Kerbosch class containing algorithm for finding all maximal cliques in a graph.
    The different implementations of the algorithm are:
    - bron_kerbosch: basic implementation
    - bron_kerbosch_with_pivot: implementation with pivot
    - bron_kerbosch_degeneracy: implementation with degeneracy ordering
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
            self.cliques.append(frozenset(R))
            return self.cliques

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

        return self.cliques

    def degeneracy_ordering(self):
        """
        Return a degeneracy ordering of the graph.
        """
        # Initialiser la liste de sortie L à la liste vide.
        L = []
        # Calculer une valeur dv pour chaque sommet v de G,
        # qui est le nombre de voisins de v qui n'est pas déjà dans L
        # (initialement, il s'agit donc du degré des sommets dans G).
        d_v = [tp[1] for tp in self.G.degree]
        # Initialiser un tableau D tel que D[i] contienne la liste des sommets v
        # qui ne sont pas déjà dans L pour lesquels dv = i.
        d = [[] for _ in range(max(d_v) + 1)]
        for v, degree in zip(self.G.nodes(), d_v):
            d[degree].append(v)

        # Initialiser la valeur k à 0.
        k = 0
        for _ in range(self.G.number_of_nodes()):
            # Parcourir les cellules du tableau D[0], D[1], ... jusqu'à trouver un i pour lequel D[i] est non-vide.
            i = 0
            while not d[i]:
                i += 1
            # Mettre k à max(k,i).
            k = max(k, i)
            # Sélectionner un sommet v de D[i], ajouter v en tête de L et le retirer de D[i].
            v = d[i].pop(0)
            L.insert(0, v)
            # Pour chaque voisin w de v qui n'est pas déjà dans L,
            # retirer une unité de dw et déplacer w de la cellule de D correspondant à la nouvelle valeur de dw.
            for w in self.G.neighbors(v):
                if w in L:
                    continue

                d[d_v[w]].remove(w)
                d_v[w] -= 1
                d[d_v[w]].append(w)

        return L

    def bron_kerbosch_degeneracy(self):
        """
        Implementation of Bron-Kerbosch algorithm with degeneracy ordering.
        """
        self.reset()
        for v in self.degeneracy_ordering():
            neighbors_v = set([n for n in self.G.neighbors(v)])
            self.bron_kerbosch_pivot(
                R=self.R.union([v]),
                P=self.P.intersection(neighbors_v),
                X=self.X.intersection(neighbors_v),
            )
            self.P.remove(v)
            self.X.add(v)
