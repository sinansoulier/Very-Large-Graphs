import networkx as nx


class NaiveCliqueSearch:
    """
    NaiveCliqueSearch class containing algorithm for finding all maximal cliques in a graph.
    This is a naive and simple implementation of the algorithm.
    """
    def __init__(self, G: nx.graph, graph_name: str = 'G'):
        self.G = G
        self.cliques = []
        self.graph_name = graph_name

    def reset(self):
        """
        Reset cliques list.
        """
        self.cliques = []

    def naive_clique_search(self):
        """
        Naive implementation of clique search.
        """
        # FIXME
        raise NotImplementedError
