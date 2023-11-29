import networkx as nx
from pyspark.sql import SparkSession

from src.bron_kerbosch.bron_kerbosch import BronKerbosch


class PySparkBronKerbosch(BronKerbosch):
    """
    PySparkBronKerbosch class containing algorithm for finding all maximal cliques in a graph.
    The algorithm is implemented using PySpark, thus it is distributed.
    The different implementations of the algorithm are:
    - bron_kerbosch_with_pivot: implementation with pivot
    - bron_kerbosch_degeneracy: implementation with degeneracy ordering
    """

    def __init__(self, G: nx.graph, graph_name: str = 'G'):
        """
        Initialize PySparkBronKerbosch class with a graph G.
        Args:
            G (nx.graph): graph
            graph_name (str): name of the graph. Defaults to 'G'.
        """
        super().__init__(G, graph_name)
        self.cliques = []

    def bron_kerbosch_degeneracy_spark(self):
        """
        Implementation of Bron-Kerbosch algorithm with degeneracy ordering.
        """
        self.reset()
        sp_c = SparkSession.builder.appName("BronKerbosch").getOrCreate()

        list_iter = []
        for v in self.degeneracy_ordering():
            neighbors_v = set([n for n in self.G.neighbors(v)])
            list_iter.append(
                (
                    v,
                    set([v]),
                    self.P.intersection(neighbors_v),
                    self.X.intersection(neighbors_v),
                )
            )
            self.P.remove(v)
            self.X.add(v)

        nodes_rdd = sp_c.sparkContext.parallelize(list_iter)
        sp_cliques = nodes_rdd\
            .map(lambda tup: self.bron_kerbosch_pivot(R=tup[1], P=tup[2], X=tup[3]))\
            .reduce(lambda x, y: set(x).union(set(y)))

        self.cliques = list(sp_cliques)

        sp_c.stop()
