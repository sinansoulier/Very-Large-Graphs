def bron_kerbosch_rec(graph, clique=[], candidates=[], excluded=[]):
    if not candidates and not excluded:
        return clique
    max_clique = clique
    for vertex in candidates[:]:
        neighbors = set(graph.neighbors(vertex))
        if vertex in neighbors:
            continue
        cur_clique = bron_kerbosch_rec(
            graph,
            clique + [vertex],
            candidates=[c for c in candidates if c in neighbors],
            excluded=[c for c in excluded if c in neighbors],
        )
        if len(cur_clique) > len(max_clique):
            max_clique = cur_clique

        candidates.remove(vertex)
        excluded.append(vertex)
    return max_clique


def bron_kerbosch(graph):
    return bron_kerbosch_rec(graph, candidates=list(graph.nodes()))
