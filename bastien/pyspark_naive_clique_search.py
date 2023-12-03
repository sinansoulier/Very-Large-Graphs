from pyspark import SparkContext
from pyspark.sql import SparkSession
import itertools
import networkx as nx
from src.naive_clique_search import is_clique
def pyspark_naive_clique_search(G):
    # search for maximal clique using pyspark
    # create spark session
    spark = SparkSession.builder.appName('SpNaiveClique').getOrCreate()
    # create spark context
    sc = spark.sparkContext
    # create rdd from nodes
    nodes_rdd = sc.parallelize(G.nodes())
    # create rdd from edges
    flatt_func = lambda n: list(itertools.combinations(G.nodes(), n))
    filtered_func = lambda nodes: is_clique(G, nodes)
    mappped_func = lambda nodes: (len(nodes), set(nodes))
    reduce_func = lambda x, y: x if x[0] > y[0] else y
    clique = nodes_rdd.flatMap(flatt_func).filter(filtered_func).map(mappped_func).reduce(reduce_func)
    # create rdd from combinations of nodes
    spark.stop()
    return clique[1]
    