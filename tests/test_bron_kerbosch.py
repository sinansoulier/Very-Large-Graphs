import pytest
import networkx as nx
import matplotlib.pyplot as plt

from src.bron_kerbosch import BronKerbosch

@pytest.mark.parametrize(
    "bk",
    [
        BronKerbosch(G=nx.erdos_renyi_graph(100, 0.1)),
        BronKerbosch(G=nx.erdos_renyi_graph(100, 0.3)),
        BronKerbosch(G=nx.erdos_renyi_graph(50, 0.5)),
        BronKerbosch(G=nx.erdos_renyi_graph(20, 0.7)),
        BronKerbosch(G=nx.erdos_renyi_graph(20, 0.9))
    ]
)
class TestBronKerbosch:
    def plot_graph(self, G: nx.graph, i: int = 1):
        nx.draw(G, with_labels=True)
        plt.savefig(f'tests/plots/graph_{i}.png', dpi=300, bbox_inches='tight')
    
    def test_bron_kerbosch(self, bk: BronKerbosch):
        self.plot_graph(bk.G, i=1)
        
        expected_cliques = [set(c) for c in nx.find_cliques(bk.G)]

        bk.bron_kerbosch(R=bk.R, P=bk.P, X=bk.X)

        assert len(bk.cliques) == len(expected_cliques)
        for clique in expected_cliques:
            assert clique in bk.cliques
        
        bk.reset()
    
    def test_bron_kerbosch_with_pivot(self, bk: BronKerbosch):
        self.plot_graph(bk.G, i=2)
        
        expected_cliques = [set(c) for c in nx.find_cliques(bk.G)]

        bk.bron_kerbosch_with_pivot(R=bk.R, P=bk.P, X=bk.X)

        assert len(bk.cliques) == len(expected_cliques)
        for clique in expected_cliques:
            assert clique in bk.cliques
        
        bk.reset()