import networkx as nx
import matplotlib.pyplot as plt
import pytest

from src.naive.naive_clique_search import NaiveCliqueSearch


@pytest.mark.parametrize(
    "ncs",
    [
        NaiveCliqueSearch(G=nx.erdos_renyi_graph(20, 0.1), graph_name='G_20_0.1'),
        NaiveCliqueSearch(G=nx.erdos_renyi_graph(20, 0.3), graph_name='G_20_0.3'),
        NaiveCliqueSearch(G=nx.erdos_renyi_graph(20, 0.5), graph_name='G_20_0.5'),
        NaiveCliqueSearch(G=nx.erdos_renyi_graph(20, 0.7), graph_name='G_20_0.7'),
        NaiveCliqueSearch(G=nx.erdos_renyi_graph(20, 0.9), graph_name='G_20_0.9'),
    ]
)
class TestNaiveCliqueSearch:
    """
    Test NaiveCliqueSearch class, defining a testsuite for each implementation of the algorithm.
    """
    def plot_graph(self, ncs: NaiveCliqueSearch):
        """
        Plot graph and save it in tests/plots folder.
        """
        nx.draw(ncs.G, with_labels=True)
        plt.savefig(f'tests/plots/{ncs.graph_name}.png', dpi=300, bbox_inches='tight')

    def test_naive_clique_search(self, ncs: NaiveCliqueSearch):
        """
        Test basic implementation of naive clique search algorithm.
        """
        self.plot_graph(ncs)

        expected_cliques = [set(c) for c in nx.find_cliques(ncs.G)]
        max_expected_clique = max(expected_cliques, key=len)

        ncs.naive_clique_search()

        assert len(ncs.max_clique) == len(max_expected_clique)

        ncs.reset()
