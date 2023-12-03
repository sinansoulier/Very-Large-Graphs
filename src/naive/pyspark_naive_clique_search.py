import itertools
from pyspark.sql import SparkSession
import networkx as nx

from src.naive.naive_clique_search import NaiveCliqueSearch


class PySparkNaiveCliqueSearch(NaiveCliqueSearch):
    """
    PySparkNaiveCliqueSearch class containing algorithm for finding all maximal cliques in a graph.
    This is a naive and simple implementation of the algorithm.
    """
    def __init__(self, G: nx.graph, graph_name: str = 'G'):
        super().__init__(G, graph_name)
        self.max_clique = set()

    def reset(self):
        """
        Reset cliques list.
        """
        self.max_clique = set()

    def naive_clique_search(self):
        """
        Naive implementation of clique search.
        """
        self.reset()

        iterations = list(range(1, self.G.number_of_nodes() + 1))
        spark = SparkSession.builder.appName('SpNaiveClique').getOrCreate()
        iterations_rdd = spark.sparkContext.parallelize(iterations)

        clique = iterations_rdd.flatMap(lambda i: list(itertools.combinations(self.G.nodes(), i))) \
            .filter(lambda nodes: self.is_clique(nodes)) \
            .map(lambda nodes: (len(nodes), set(nodes))) \
            .reduce(lambda x, y: x if x[0] > y[0] else y)

        self.max_clique = clique[1]
        spark.stop()
