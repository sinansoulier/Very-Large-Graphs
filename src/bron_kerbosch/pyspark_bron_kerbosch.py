import networkx as nx
import concurrent.futures
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

    def bron_kerbosch_pivot_threaded(self, R: set, P: set, X: set):
        """
        Implementation of Bron-Kerbosch algorithm with pivot, using multithreading.

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

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for v in list(P.difference(neighbors_u)):
                neighbors_v = set([n for n in self.G.neighbors(v)])
                future = executor.submit(
                    self.bron_kerbosch_pivot,
                    R.union([v]),
                    P.intersection(neighbors_v),
                    X.intersection(neighbors_v),
                )
                P.remove(v)
                X.add(v)

                futures.append(future)

            concurrent.futures.wait(futures)

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
        print(nodes_rdd)
        r_cliques = nodes_rdd.map(lambda tup: self.bron_kerbosch_pivot(R=tup[1], P=tup[2], X=tup[3]))

        self.cliques = list(r_cliques.reduce(lambda x, y: set(x).union(set(y))))

        sp_c.stop()
