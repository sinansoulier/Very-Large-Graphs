import networkx as nx
import itertools


class NaiveCliqueSearch:
    """
    NaiveCliqueSearch class containing algorithm for finding all maximal cliques in a graph.
    This is a naive and simple implementation of the algorithm.
    """
    def __init__(self, G: nx.graph, graph_name: str = 'G'):
        self.G = G
        self.max_clique = set()
        self.graph_name = graph_name

    def reset(self):
        """
        Reset cliques list.
        """
        self.max_clique = set()

    def is_clique(self, nodes: list):
        """
        Check if a set of nodes is a clique.
        Args:
            nodes (list): list of nodes
        Returns:
            bool: True if nodes is a clique, False otherwise
        """
        for u, v in itertools.combinations(nodes, 2):
            if v not in self.G.neighbors(u):
                return False
        return True

    def naive_clique_search(self):
        """
        Naive implementation of clique search.
        """
        self.reset()
        max_clique_size = 0

        for i in range(1, self.G.number_of_nodes() + 1):
            for nodes in itertools.combinations(self.G.nodes(), i):
                if len(nodes) > max_clique_size and self.is_clique(nodes):
                    self.max_clique = set(nodes)
                    max_clique_size = len(self.max_clique)
