import pytest
import matplotlib.pyplot as plt
import networkx as nx

from src.naive.pyspark_naive_clique_search import PySparkNaiveCliqueSearch


@pytest.mark.parametrize(
    "ncs",
    [
        PySparkNaiveCliqueSearch(G=nx.erdos_renyi_graph(20, 0.1), graph_name='Spark_G_20_0.1'),
        PySparkNaiveCliqueSearch(G=nx.erdos_renyi_graph(20, 0.3), graph_name='Spark_G_20_0.3'),
        PySparkNaiveCliqueSearch(G=nx.erdos_renyi_graph(20, 0.5), graph_name='Spark_G_20_0.5'),
        PySparkNaiveCliqueSearch(G=nx.erdos_renyi_graph(20, 0.7), graph_name='Saprk_G_20_0.7'),
        PySparkNaiveCliqueSearch(G=nx.erdos_renyi_graph(20, 0.9), graph_name='Spark_G_20_0.9'),
    ]
)
class TestPySparkNaiveCliqueSearch:
    """
    Test NaiveCliqueSearch class, defining a testsuite for each implementation of the algorithm.
    """
    def plot_graph(self, ncs: PySparkNaiveCliqueSearch):
        """
        Plot graph and save it in tests/plots folder.
        """
        nx.draw(ncs.G, with_labels=True)
        plt.savefig(f'tests/plots/{ncs.graph_name}.png', dpi=300, bbox_inches='tight')

    def test_naive_clique_search(self, ncs: PySparkNaiveCliqueSearch):
        """
        Test basic implementation of naive clique search algorithm.
        """
        self.plot_graph(ncs)

        expected_cliques = [set(c) for c in nx.find_cliques(ncs.G)]
        max_expected_clique = max(expected_cliques, key=len)

        ncs.naive_clique_search()

        assert len(ncs.max_clique) == len(max_expected_clique)

        ncs.reset()
