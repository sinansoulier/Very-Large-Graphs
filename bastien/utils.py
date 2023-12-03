import random


def clique(n_clique):
    for i in range(1, n_clique + 1):
        for j in range(i + 1, n_clique + 1):
            yield (i, j)


def edges_list(n_clique, additional_nodes):
    for i in range(n_clique + 1, n_clique + 1 + additional_nodes):
        yield (
            random.randint(0, n_clique + additional_nodes),
            random.randint(0, n_clique + additional_nodes),
        )
