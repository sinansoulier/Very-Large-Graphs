import pytest
import networkx as nx
import matplotlib.pyplot as plt

from src.bron_kerbosch.pyspark_bron_kerbosch import PySparkBronKerbosch


@pytest.mark.parametrize(
    "bk",
    [
        PySparkBronKerbosch(G=nx.erdos_renyi_graph(20, 0.1), graph_name='PySpark_G_20_0.1'),
        PySparkBronKerbosch(G=nx.erdos_renyi_graph(20, 0.3), graph_name='PySpark_G_20_0.3'),
        PySparkBronKerbosch(G=nx.erdos_renyi_graph(20, 0.5), graph_name='PySpark_G_20_0.5'),
        PySparkBronKerbosch(G=nx.erdos_renyi_graph(20, 0.7), graph_name='PySpark_G_20_0.7'),
        PySparkBronKerbosch(G=nx.erdos_renyi_graph(20, 0.9), graph_name='PySpark_G_20_0.9'),
    ]
)
class TestPySparkBronKerbosch:
    """
    Test BronKerbosch class, defining a testsuite for each implementation of the algorithm.
    """
    def plot_graph(self, bk: PySparkBronKerbosch):
        """
        Plot graph and save it in tests/plots folder.
        """
        nx.draw(bk.G, with_labels=True)
        plt.savefig(f'tests/plots/{bk.graph_name}.png', dpi=300, bbox_inches='tight')

    def test_bron_kerbosch_degeneracy(self, bk: PySparkBronKerbosch):
        """
        Test implementation of Bron-Kerbosch algorithm with degeneracy ordering.
        """
        self.plot_graph(bk)

        expected_cliques = [set(c) for c in nx.find_cliques(bk.G)]

        bk.bron_kerbosch_degeneracy_spark()

        assert len(bk.cliques) == len(expected_cliques)
        for clique in expected_cliques:
            assert clique in bk.cliques

        bk.reset()
