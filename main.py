import networkx as nx
import matplotlib.pyplot as plt
import random


def evolve_network(n, m, difficultCoefficient):
    """n, m - dimension of generated grid(map)
        difficultCoefficient - probability of removing edge
    """
 # Check if graph is connected
    connectedGraphFlag = False
    while not connectedGraphFlag:

        # Generate grid
        G = nx.grid_2d_graph(n, m)
        # Decrease n, m because of start from zero
        nZ = n - 1
        mZ = m - 1

        # Remove boundary edges
        for i in range(mZ):
            G.remove_edge((0, i), (0, i + 1))
            G.remove_edge((nZ, i), (nZ, i + 1))
        for i in range(nZ):
            G.remove_edge((i, 0), (i + 1, 0))
            G.remove_edge((i, mZ), (i + 1, mZ))

        # Remove corner nodes
        G.remove_node((0, 0))
        G.remove_node((0, mZ))
        G.remove_node((nZ, 0))
        G.remove_node((nZ, mZ))

        # Randomly remove edges
        for edge in G.edges():
            if random.random() < difficultCoefficient:
                G.remove_edge(*edge)

        # Generate node list for subraph
        mapNodes = []
        for i in range(1, nZ):
            for j in range(1, mZ):
                mapNodes.append((i, j))

        # Check if subgraph is connected
        mapgraph = G.subgraph(mapNodes)
        connectedGraphFlag = nx.is_connected(mapgraph)

    print mapgraph.degree().values()
    # Graph layout
    pos = {}
    for n in G:
        pos[n] = (n[0], n[1])

    # Generate graph image
    nx.draw(G, pos)
    plt.show()

evolve_network(5, 5, 0.35)
