import networkx as nx


#R : L'ensemble des sommets actuellement sélectionnés dans le clique.
#P : L'ensemble des candidats, sommets qui sont connectés à tous les sommets dans R et peuvent potentiellement être ajoutés à R.
#X : L'ensemble des sommets exclus, déjà considérés avec les sommets actuels de R et qui ne peuvent pas former un clique maximal avec eux.
def bron_kerbosch(R, P, X, G, cliques=None):
    """
    Implémentation de l'algorithme Bron-Kerbosch sans pivot.

    Args:
    R, P, X : Ensembles de sommets.
    G : Graphique networkx.
    cliques : Liste accumulant les cliques trouvées.
    """
    if cliques is None:
        cliques = []

    if not P and not X:
        cliques.append(R)
        return cliques

    new_cliques = cliques
    for v in list(P):
        bron_kerbosch(R.union([v]), P.intersection(G.neighbors(v)), X.intersection(G.neighbors(v)), G, new_cliques)
        P.remove(v)
        X.add(v)
    
    return new_cliques


def bron_kerbosch_pivot(R, P, X, G, cliques=None):
    if cliques is None:
        cliques = []

    if not P and not X:
        cliques.append(sorted(list(R)))  # Convertir en liste et trier
        return cliques

    # Choisir un sommet pivot u dans P union X
    u = sorted(list(P.union(X)))[0]
    N_v = set(G.neighbors(u))

    for v in sorted(list(P.difference(N_v))):
        bron_kerbosch_pivot(R.union([v]), P.intersection(G.neighbors(v)), X.intersection(G.neighbors(v)), G, cliques)
        P.remove(v)
        X.add(v)

    return cliques



def degenerescence(G):
    # Initialiser la liste de sortie L à la liste vide.
    L = []
    # Calculer le degré de chaque sommet et le stocker dans un dictionnaire.
    dv = {v: len(list(G.neighbors(v))) for v in G.nodes()}
    # Initialiser la liste D de listes de sommets indexées par leur degré.
    D = [[] for _ in range(max(dv.values()) + 1)]
    for v, d in dv.items():
        D[d].append(v)
    
    k = 0
    for _ in range(G.number_of_nodes()):
        for i in range(len(D)):
            if D[i]:
                k = max(k, i)
                break
        v = D[i].pop()
        L.insert(0, v)
        # Pour chaque voisin w de v, si w n'est pas dans L, 
        # alors décrémenter son degré et le déplacer dans la liste de degré inférieur.
        for w in G.neighbors(v):
            if w not in L:
                dw = dv[w]
                D[dw].remove(w)
                D[dw - 1].append(w)
                dv[w] -= 1
    
    return k, L


def bron_kerbosch_degen(G, cliques=None):
    if cliques is None:
        cliques = []

    _, deg_order = degenerescence(G)
    P = set(G.nodes())
    R = set()
    X = set()

    for v in deg_order:
        N_v = set(G.neighbors(v))
        bron_kerbosch_pivot(R.union([v]), P.intersection(N_v), X.intersection(N_v), G, cliques)
        P.remove(v)
        X.add(v)

    return cliques






