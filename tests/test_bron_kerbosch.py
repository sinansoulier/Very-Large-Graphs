import pytest
import networkx as nx
import matplotlib.pyplot as plt

from src.bron_kerbosch import BronKerbosch


@pytest.mark.parametrize(
    "bk",
    [
        BronKerbosch(G=nx.erdos_renyi_graph(100, 0.1), graph_name='G_100_0.1'),
        BronKerbosch(G=nx.erdos_renyi_graph(100, 0.3), graph_name='G_100_0.3'),
        BronKerbosch(G=nx.erdos_renyi_graph(50, 0.5), graph_name='G_50_0.5'),
        BronKerbosch(G=nx.erdos_renyi_graph(20, 0.7), graph_name='G_20_0.7'),
        BronKerbosch(G=nx.erdos_renyi_graph(20, 0.9), graph_name='G_20_0.9'),
    ]
)
class TestBronKerbosch:
    """
    Test BronKerbosch class, defining a testsuite for each implementation of the algorithm.
    """
    def plot_graph(self, bk: BronKerbosch):
        """
        Plot graph and save it in tests/plots folder.
        """
        nx.draw(bk.G, with_labels=True)
        plt.savefig(f'tests/plots/{bk.graph_name}.png', dpi=300, bbox_inches='tight')

    def test_bron_kerbosch(self, bk: BronKerbosch):
        """
        Test basic implementation of Bron-Kerbosch algorithm.
        """
        self.plot_graph(bk)

        expected_cliques = [set(c) for c in nx.find_cliques(bk.G)]

        bk.bron_kerbosch(R=bk.R, P=bk.P, X=bk.X)

        assert len(bk.cliques) == len(expected_cliques)
        for clique in expected_cliques:
            assert clique in bk.cliques

        bk.reset()

    def test_bron_kerbosch_with_pivot(self, bk: BronKerbosch):
        """
        Test implementation of Bron-Kerbosch algorithm with pivot.
        """
        self.plot_graph(bk)

        expected_cliques = [set(c) for c in nx.find_cliques(bk.G)]

        bk.bron_kerbosch_pivot(R=bk.R, P=bk.P, X=bk.X)

        assert len(bk.cliques) == len(expected_cliques)
        for clique in expected_cliques:
            assert clique in bk.cliques

        bk.reset()

    def test_bron_kerbosch_degeneracy(self, bk: BronKerbosch):
        """
        Test implementation of Bron-Kerbosch algorithm with degeneracy ordering.
        """
        self.plot_graph(bk)

        expected_cliques = [set(c) for c in nx.find_cliques(bk.G)]

        bk.bron_kerbosch_degeneracy()

        assert len(bk.cliques) == len(expected_cliques)
        for clique in expected_cliques:
            assert clique in bk.cliques

        bk.reset()
