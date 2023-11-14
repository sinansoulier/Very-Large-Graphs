import networkx as nx

class BronKerbosch:
    def __init__(self, G: nx.graph):
        self.G = G
        self.cliques = []
        
        self.R = set()
        self.P = set(G.nodes)
        self.X = set()

    def bron_kerbosch(self, R: set, P: set, X: set):
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

    def bron_kerbosch_with_pivot(self, R: set, P: set, X: set):
        # FIXME
        raise NotImplementedError

    def reset(self):
        self.cliques = []
        self.R = set()
        self.P = set(self.G.nodes)
        self.X = set()