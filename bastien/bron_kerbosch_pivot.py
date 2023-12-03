import networkx as nx


def bron_kerbosch_pivot_rec(graph, R=[], P=[], X=[], pivot_func=None):
    if not P and not X:
        return R
    max_clique = R
    pivot = choose_pivot(P, X, pivot_func=pivot_func)
    vertices_to_iterate = [c for c in P if c not in graph.neighbors(pivot)]
    for vertex in vertices_to_iterate:
        neighbors = set(graph.neighbors(vertex))
        if vertex in neighbors:
            continue
        cur_clique = bron_kerbosch_pivot_rec(
            graph,
            R + [vertex],
            P=[c for c in P if c in neighbors],
            X=[c for c in X if c in neighbors],
        )
        if len(cur_clique) > len(max_clique):
            max_clique = cur_clique

        P.remove(vertex)
        X.append(vertex)
    return max_clique


def bron_kerbosch_pivot(graph, pivot_func=None):
    return bron_kerbosch_pivot_rec(graph, P=list(graph.nodes()), pivot_func=pivot_func)


def choose_pivot(P, X, pivot_func):
    combined_set = set(P + X)
    return pivot_func(combined_set) if pivot_func else next(iter(combined_set))
