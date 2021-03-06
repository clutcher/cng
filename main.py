import random

import networkx as nx
import matplotlib.pyplot as plt


class GameMap(object):
    """Game map generating class"""

    def __init__(self, n, m, difficultCoefficient=0.5, exclude=0, allTileTypes=False, excludeDegree=0):
        self.n = n + 2
        self.m = m + 2
        self.difficultCoefficient = difficultCoefficient
        self.diagonalNodes = []
        self.throughNodes = []
        self.throughEdges = []
        self.taskObjects = {}
        if excludeDegree:
            self.excludeDegree = excludeDegree
        else:
            self.excludeDegree = []
        if exclude:
            self.excludedNodes = exclude
        else:
            self.excludedNodes = []
        self.allTileTypes = allTileTypes
        # Generate grid
        self.G = nx.grid_2d_graph(self.n, self.m)

    def check_edge_in_edgelist(self, edgeCheck, edgeList=None):
        if not edgeList:
            edgeList = self.G.edges()
        for edge in edgeList:
            if (edgeCheck[0] in edge) and (edgeCheck[1] in edge):
                return 1
        return 0

    def check_node_in_edgelist(self, node, edgeList):
        for edge in edgeList:
            if (node in edge):
                # print edge, edgeCheck
                return edge
        return 0

    def get_simple_degree(self, node):
        degree = 0
        edgePosList = [(node, (node[0], node[1] + 1)), (node, (node[0] + 1, node[1])), (
            node, (node[0], node[1] - 1)), (node, (node[0] - 1, node[1]))]
        for edge in self.G.edges(node):
            if self.check_edge_in_edgelist(edge, edgePosList):
                degree = degree + 1
        return degree

    def get_simple_edges(self, node):
        edgeList = self.G.edges(node)
        edgePosList = [(node, (node[0], node[1] + 1)), (node, (node[0] + 1, node[1])), (
            node, (node[0], node[1] - 1)), (node, (node[0] - 1, node[1]))]
        for edge in edgeList:
            if not self.check_edge_in_edgelist(edge, edgePosList):
                edgeList.remove(edge)
        return edgeList

    def generate_full_connected_grid(self):
        # Additional clean
        self.G = nx.grid_2d_graph(self.n, self.m)
        # Decrease n, m because of start from zero
        nZ = self.n - 1
        mZ = self.m - 1

        # Add diagonalic connections
        for i in xrange(nZ):
            for j in xrange(mZ):
                self.G.add_edge((i, j), (i + 1, j + 1))
                if (j - 1) >= 0:
                    self.G.add_edge((i, j), (i + 1, j - 1))
                else:
                    self.G.add_edge((i, j + mZ), (i + 1, j + mZ - 1))

        # Add interedges
        for i in xrange(1, nZ):
            for j in xrange(1, mZ):
                if (j + 2) < (self.m - 2):
                    self.G.add_edge((i, j), (i, j + 2))
                if (i + 2) < (self.n - 2):
                    self.G.add_edge((i, j), (i + 2, j))
                if (j - 2) >= 0:
                    self.G.add_edge((i, j), (i, j - 2))
                if (i - 2) >= 0:
                    self.G.add_edge((i, j), (i - 2, j))

        # Remove boundary edges
        for i in range(nZ):
            self.G.remove_edge((i, 0), (i + 1, 0))
            self.G.remove_edge((i, mZ), (i + 1, mZ))
        for j in range(mZ):
            self.G.remove_edge((0, j), (0, j + 1))
            self.G.remove_edge((nZ, j), (nZ, j + 1))

        # Remove corner nodes
        self.G.remove_node((0, 0))
        self.G.remove_node((0, mZ))
        self.G.remove_node((nZ, 0))
        self.G.remove_node((nZ, mZ))

        # Remove excluded(bondary) edges
        for node in self.excludedNodes:
            self.G.remove_edges_from(self.G.edges(node))
        return 1

    def find_tile_for_network_remade(self, node, degreePosible=None):
        i = node[0]
        j = node[1]
        self.clean_added_edges()
        if degreePosible:
            degree = degreePosible
        else:
            degree = self.get_simple_degree(node)

        if degree == 0:
            edge = ((i - 1, j), (i, j + 1))
            edge2 = ((i, j - 1), (i + 1, j))
            edge3 = ((i - 1, j), (i, j - 1))
            edge4 = ((i, j + 1), (i + 1, j))
            if self.check_edge_in_edgelist(edge) and self.check_edge_in_edgelist(edge2):
                return 3
            elif self.check_edge_in_edgelist(edge3) and self.check_edge_in_edgelist(edge4):
                return 3
            else:
                return -1

        elif degree == 1:
            edge = ((i, j), (i + 1, j + 1))
            edge2 = ((i, j), (i + 1, j - 1))
            edge3 = ((i, j), (i - 1, j - 1))
            edge4 = ((i, j), (i - 1, j + 1))

            countDiag = self.check_edge_in_edgelist(edge) + self.check_edge_in_edgelist(
                edge2) + self.check_edge_in_edgelist(edge3) + self.check_edge_in_edgelist(edge4)
            if countDiag == 2:
                return 2
            else:
                return -1

        elif degree == 2:
            edge = ((i, j), (i + 1, j))
            edge2 = ((i, j), (i, j - 1))
            edge3 = ((i, j), (i, j + 1))
            edge4 = ((i, j), (i - 1, j))

            if self.check_edge_in_edgelist(edge) and self.check_edge_in_edgelist(edge2):
                return 1
            elif self.check_edge_in_edgelist(edge) and self.check_edge_in_edgelist(edge3):
                return 1
            elif self.check_edge_in_edgelist(edge3) and self.check_edge_in_edgelist(edge4):
                return 1
            elif self.check_edge_in_edgelist(edge2) and self.check_edge_in_edgelist(edge4):
                return 1

            edge5 = ((i, j + 1), (i, j - 1))
            edge6 = ((i - 1, j), (i + 1, j))

            if self.check_edge_in_edgelist(edge) and self.check_edge_in_edgelist(edge4) and self.check_edge_in_edgelist(
                    edge5):
                return 5
            elif self.check_edge_in_edgelist(edge2) and self.check_edge_in_edgelist(
                    edge3) and self.check_edge_in_edgelist(edge6):
                return 5
            else:
                return -1

        elif degree == 3:
            edge = ((i, j), (i + 1, j))
            edge2 = ((i, j), (i, j - 1))
            edge3 = ((i, j), (i, j + 1))
            edge4 = ((i, j), (i - 1, j))

            if self.check_edge_in_edgelist(edge) and self.check_edge_in_edgelist(edge2) and self.check_edge_in_edgelist(
                    edge3):
                return 2
            elif self.check_edge_in_edgelist(edge) and self.check_edge_in_edgelist(
                    edge2) and self.check_edge_in_edgelist(edge4):
                return 2
            elif self.check_edge_in_edgelist(edge) and self.check_edge_in_edgelist(
                    edge3) and self.check_edge_in_edgelist(edge4):
                return 2
            elif self.check_edge_in_edgelist(edge3) and self.check_edge_in_edgelist(
                    edge3) and self.check_edge_in_edgelist(edge4):
                return 2
            else:
                return -1
        elif degree == 4:
            edge = ((i, j), (i + 1, j))
            edge2 = ((i, j), (i, j - 1))
            edge3 = ((i, j), (i, j + 1))
            edge4 = ((i, j), (i - 1, j))

            if self.check_edge_in_edgelist(edge) and self.check_edge_in_edgelist(edge2) and self.check_edge_in_edgelist(
                    edge3) and self.check_edge_in_edgelist(edge4):
                return 4
            else:
                return -1
        else:
            return -1

    def remove_simetric_diagonal_edges(self):
        # Remove simmetric diagonal edges
        for edge in self.G.edges():
            nodeS = edge[0]
            nodeE = edge[1]
            if abs(nodeS[0] - nodeE[0]) == 1 and abs(nodeS[1] - nodeE[1]) == 1:
                if (nodeS[0] + 1 == nodeE[0] and nodeS[1] + 1 == nodeE[1]) or (
                                    nodeS[0] - 1 == nodeE[0] and nodeS[1] - 1 == nodeE[1]):
                    simmetricEdge = (
                        (nodeS[0] - 1, nodeS[1] + 1), (nodeE[0] - 1, nodeE[1] + 1))
                    simmetricEdge2 = (
                        (nodeS[0] + 1, nodeS[1] - 1), (nodeE[0] + 1, nodeE[1] - 1))
                    if self.check_edge_in_edgelist(simmetricEdge):
                        # print str(edge) + ' 1'
                        pass
                    elif self.check_edge_in_edgelist(simmetricEdge2):
                        # print str(edge) + ' 2'
                        pass
                    else:
                        # print 'removed  - ' + str(edge)
                        self.G.remove_edge(*edge)
                else:
                    simmetricEdge = (
                        (nodeS[0] + 1, nodeS[1] + 1), (nodeE[0] + 1, nodeE[1] + 1))
                    simmetricEdge2 = (
                        (nodeS[0] - 1, nodeS[1] - 1), (nodeE[0] - 1, nodeE[1] - 1))
                    if self.check_edge_in_edgelist(simmetricEdge):
                        # print str(edge) + ' 3'
                        pass
                    elif self.check_edge_in_edgelist(simmetricEdge2):
                        # print str(edge) + ' 4'
                        pass
                    else:
                        # print 'removed  - ' + str(edge)
                        self.G.remove_edge(*edge)

        return 1

    def remove_through_edges(self):
        for edge in self.G.edges():
            nodeS = edge[0]
            nodeE = edge[1]
            firstVariantCheck = abs(nodeS[0] - nodeE[0]) == 2
            secondVariantCheck = abs(nodeS[1] - nodeE[1]) == 2
            if firstVariantCheck or secondVariantCheck:
                if firstVariantCheck:
                    # Center node
                    i = (nodeS[0] + nodeE[0]) / 2
                    j = nodeS[1]

                    edge1 = ((i, j), (i, j + 1))
                    edge2 = ((i, j), (i, j - 1))

                    if self.check_edge_in_edgelist(edge1) and self.check_edge_in_edgelist(edge2):
                        pass
                    else:
                        self.G.remove_edge(*edge)
                else:
                    # Center node
                    i = nodeS[0]
                    j = (nodeS[1] + nodeE[1]) / 2

                    edge1 = ((i, j), (i + 1, j))
                    edge2 = ((i, j), (i - 1, j))

                    if self.check_edge_in_edgelist(edge1) and self.check_edge_in_edgelist(edge2):
                        pass
                    else:
                        self.G.remove_edge(*edge)
        return 1

    def randomize_removing_edges(self):
        # Randomly remove edges
        for edge in self.G.edges():
            if random.random() < self.difficultCoefficient:
                self.G.remove_edge(*edge)

        self.remove_simetric_diagonal_edges()

        return 1

    def randomize_add_edges(self, node):
        """Add edges when can`t fin tile"""

        def find_simetric_edge(edgeExist):
            if edgeExist[0] != node:
                nodeE = edgeExist[0]
            else:
                nodeE = edgeExist[1]
            if nodeE[0] - node[0] == 0:
                symetricEdge = (
                    node, (node[0], node[1] - (nodeE[1] - node[1])))
            else:
                symetricEdge = (
                    node, (node[0] - (nodeE[0] - node[0]), node[1]))
            return symetricEdge

        nodeDegree = self.get_simple_degree(node)
        edgePosList = [(node, (node[0], node[1] + 1)), (node, (node[0] + 1, node[1])), (
            node, (node[0], node[1] - 1)), (node, (node[0] - 1, node[1]))]

        if self.diagonalNodes:
            for nodeDiagonal in self.diagonalNodes:
                # print nodeDiagonal, self.check_node_in_edgelist(nodeDiagonal,
                # edgePosList)
                while self.check_node_in_edgelist(nodeDiagonal, edgePosList):
                    edgePosList.remove(
                        self.check_node_in_edgelist(nodeDiagonal, edgePosList))
        if self.throughNodes:
            for nodeThrough in self.throughNodes:
                # print nodeDiagonal, self.check_node_in_edgelist(nodeDiagonal,
                # edgePosList)
                while self.check_node_in_edgelist(nodeThrough, edgePosList):
                    edgePosList.remove(
                        self.check_node_in_edgelist(nodeThrough, edgePosList))

        if nodeDegree == 0 and self.G.degree(node) == 2:
            # tile = random.randint(1, 2)
            tile = 2
            if tile == 2:
                edgeList = self.G.edges(node)
                if edgeList[0][0] != node:
                    nodetS = edgeList[0][0]
                else:
                    nodetS = edgeList[0][1]

                if edgeList[1][0] != node:
                    nodetE = edgeList[1][0]
                else:
                    nodetE = edgeList[1][1]

                iN = (nodetS[0] + nodetE[0]) / 2
                yN = (nodetS[1] + nodetE[1]) / 2
                nodeE = ((iN), (yN))
                edgeList = []
                edge = (node, nodeE)
                edge2 = (
                    node, ((node[0] - (nodeE[0] - node[0])), ((node[1] - (nodeE[1] - node[1])))))
                edgeList.append(edge)
                edgeList.append(edge2)

                if edgePosList:
                    edge = edgePosList[random.randint(0, len(edgePosList) - 1)]
                    self.G.add_edge(*edge)
                    # else:
                    #     print 'Error: ' + str(node) + ' with degree ' + str(nodeDegree)

        elif nodeDegree == 0:
            # tile = random.randint(1, 2)

            tile = 1
            if tile == 1 and (len(edgePosList) - 1) > -1:
                edgeExist = edgePosList[
                    random.randint(0, len(edgePosList) - 1)]
                self.G.add_edge(*edgeExist)
                edgePosList.remove(edgeExist)
                if find_simetric_edge(edgeExist) in edgePosList:
                    edgePosList.remove(find_simetric_edge(edgeExist))

                if edgePosList:
                    edge = edgePosList[random.randint(0, len(edgePosList) - 1)]
                    self.G.add_edge(*edge)
                    # else:
                    #     print 'Error: ' + str(node) + ' with degree ' + str(nodeDegree)

        elif nodeDegree == 1:

            edgeExist = self.get_simple_edges(node)[0]

            # tile = random.randint(1, 2)
            tile = 1
            if tile == 1:
                if edgeExist in edgePosList:
                    edgePosList.remove(edgeExist)
                if find_simetric_edge(edgeExist) in edgePosList:
                    edgePosList.remove(find_simetric_edge(edgeExist))

                if edgePosList:
                    edge = edgePosList[random.randint(0, len(edgePosList) - 1)]
                    self.G.add_edge(*edge)
                    # else:
                    #     print 'Error: ' + str(node) + ' with degree ' + str(nodeDegree)
        elif nodeDegree == 2:
            edgeExist = self.get_simple_edges(node)[0]
            edgeSymetric = self.get_simple_edges(node)[1]
            self.G.remove_edge(*edgeSymetric)
            if edgeExist in edgePosList:
                edgePosList.remove(edgeExist)
            if edgeSymetric in edgePosList:
                edgePosList.remove(edgeSymetric)

            if edgePosList:
                edge = edgePosList[random.randint(0, len(edgePosList) - 1)]
                self.G.add_edge(*edge)
                # else:
                #     print 'Error: ' + str(node) + ' with degree ' + str(nodeDegree)
        elif self.G.degree(node) == 1:
            print edgePosList

        return 1


    def add_edges_breakNode(self, node):
        def find_simetric_edge(edgeExist):
            if edgeExist[0] != node:
                nodeE = edgeExist[0]
            else:
                nodeE = edgeExist[1]
            if nodeE[0] - node[0] == 0:
                symetricEdge = (
                    node, (node[0], node[1] - (nodeE[1] - node[1])))
            else:
                symetricEdge = (
                    node, (node[0] - (nodeE[0] - node[0]), node[1]))
            return symetricEdge

        nodeDegree = self.get_simple_degree(node)
        edgePosList = [(node, (node[0], node[1] + 1)), (node, (node[0] + 1, node[1])), (
            node, (node[0], node[1] - 1)), (node, (node[0] - 1, node[1]))]
        if self.throughNodes:
            for nodeThrough in self.throughNodes:
                # print nodeDiagonal, self.check_node_in_edgelist(nodeDiagonal,
                # edgePosList)
                while self.check_node_in_edgelist(nodeThrough, edgePosList):
                    edgePosList.remove(
                        self.check_node_in_edgelist(nodeThrough, edgePosList))
        if nodeDegree == 0:
            i = node[0]
            j = node[1]

            edge = ((i, j), (i + 1, j))
            edge2 = ((i, j), (i, j - 1))
            edge3 = ((i, j), (i, j + 1))
            edge4 = ((i, j), (i - 1, j))

            self.G.add_edge(*edge)
            self.G.add_edge(*edge2)
            self.G.add_edge(*edge3)
            self.G.add_edge(*edge4)

            self.clean_added_edges()

        if nodeDegree == 1 and (self.G.degree(node) == 1 or self.G.degree(node) == 0 or self.G.degree(node) == 2):
            edgeExist = self.get_simple_edges(node)[0]
            if edgeExist in edgePosList:
                edgePosList.remove(edgeExist)
            if find_simetric_edge(edgeExist) in edgePosList:
                edgePosList.remove(find_simetric_edge(edgeExist))
            if edgePosList:
                edge = edgePosList[random.randint(0, len(edgePosList) - 1)]
                self.G.add_edge(*edge)

        elif nodeDegree == 2 and self.G.degree(node) == 2:
            edgeExist = self.get_simple_edges(node)
            for edge in edgeExist:
                try:
                    edgePosList.remove((edge[0], edge[1]))
                except:
                    pass
                try:
                    edgePosList.remove((edge[1], edge[0]))
                except:
                    pass
            if edgePosList:
                edge = edgePosList[random.randint(0, len(edgePosList) - 1)]
                self.G.add_edge(*edge)

        return 1

    def remade_network_by_tile(self):
        # Find difficult tiles
        self.remade_for_difficult_tile()

        # Add missing edges for tiles
        repeatTilefind = 0
        allTilesExist = False

        # iRange = sorted(range(1, self.n - 1), key=lambda k: random.random())
        # jRange = sorted(range(1, self.m - 1), key=lambda k: random.random())

        # while True:
        fallBackNode = []
        while not allTilesExist:
            allTilesExist = True
            for i in range(1, self.n - 1):
                for j in range(1, self.m - 1):
                    node = (i, j)
                    if node not in self.excludedNodes:
                        while (self.find_tile_for_network_remade(node) == -1) and repeatTilefind < 5:
                            allTilesExist = False
                            self.randomize_add_edges(node)
                            repeatTilefind = repeatTilefind + 1
                        if self.find_tile_for_network_remade(node) == -1:
                            fallBackNode.append(node)

        # Check remade
        self.throughEdges = []
        self.throughNodes = []
        self.diagonalNodes = []
        self.remade_for_difficult_tile()

        # Remade fallback
        fallBackNode = list(set(fallBackNode))
        # if fallBackNode == []:
        #     break
        # else:
        for breakNode in fallBackNode:
            self.add_edges_breakNode(breakNode)

        return 1

    def remade_for_difficult_tile(self):
        """ Finding tile 3 and 5"""
        # Tile 3
        tileCount = 0
        edgesRestore = []

        iRange = sorted(range(1, self.n - 1), key=lambda k: random.random())
        jRange = sorted(range(1, self.m - 1), key=lambda k: random.random())

        for i in iRange:
            for j in jRange:
                node = (i, j)
                edge = ((i - 1, j), (i, j + 1))
                edge2 = ((i, j - 1), (i + 1, j))
                edge3 = ((i - 1, j), (i, j - 1))
                edge4 = ((i, j + 1), (i + 1, j))
                if node not in self.excludedNodes:
                    firstVariantCheck = self.check_edge_in_edgelist(
                        edge) and self.check_edge_in_edgelist(edge2)
                    secondVariantCheck = self.check_edge_in_edgelist(
                        edge3) and self.check_edge_in_edgelist(edge4)

                    if firstVariantCheck and secondVariantCheck:
                        if random.randint(1, 2) == 1:
                            self.G.remove_edge(*edge)
                            self.G.remove_edge(*edge2)
                        else:
                            self.G.remove_edge(*edge3)
                            self.G.remove_edge(*edge4)

                    if firstVariantCheck or secondVariantCheck:
                        tileCount = tileCount + 1
                        if tileCount > int(round(((self.n - 2) * (self.m - 2) - len(self.excludedNodes)) / 4.5)):
                            if self.check_edge_in_edgelist(edge) and self.check_edge_in_edgelist(edge2):
                                self.G.remove_edge(*edge)
                                self.G.remove_edge(*edge2)
                            elif self.check_edge_in_edgelist(edge3) and self.check_edge_in_edgelist(edge4):
                                self.G.remove_edge(*edge3)
                                self.G.remove_edge(*edge4)
                        else:
                            if node not in self.diagonalNodes:
                                self.diagonalNodes.append(node)
                            if (self.check_edge_in_edgelist(edge) and self.check_edge_in_edgelist(edge2)):
                                edgesRestore.append(edge)
                                edgesRestore.append(edge2)
                            else:
                                edgesRestore.append(edge3)
                                edgesRestore.append(edge4)
                            for edgeNode in self.G.edges(node):
                                self.G.remove_edge(*edgeNode)
                else:
                    try:
                        self.G.remove_edge(*edge)
                    except:
                        pass
                    try:
                        self.G.remove_edge(*edge2)
                    except:
                        pass
                    try:
                        self.G.remove_edge(*edge3)
                    except:
                        pass
                    try:
                        self.G.remove_edge(*edge4)
                    except:
                        pass

        self.remove_simetric_diagonal_edges()

        for edgeR in edgesRestore:
            self.G.add_edge(*edgeR)

        # Tile 5

        self.remove_through_edges()

        tileCount = 0
        edgesRestore = []
        for i in iRange:
            for j in jRange:
                node = (i, j)
                edge = ((i, j), (i + 1, j))
                edge2 = ((i, j), (i - 1, j))
                edge3 = ((i, j + 1), (i, j - 1))

                edge4 = ((i, j), (i, j - 1))
                edge5 = ((i, j), (i, j + 1))
                edge6 = ((i - 1, j), (i + 1, j))

                if node not in self.excludedNodes:
                    firstVariantCheck = self.check_edge_in_edgelist(
                        edge) and self.check_edge_in_edgelist(edge2) and self.check_edge_in_edgelist(edge3)
                    secondVariantCheck = self.check_edge_in_edgelist(
                        edge4) and self.check_edge_in_edgelist(edge5) and self.check_edge_in_edgelist(edge6)

                    if firstVariantCheck or secondVariantCheck:
                        tileCount = tileCount + 1
                        if tileCount > int(round(((self.n - 2) * (self.m - 2) - len(self.excludedNodes)) / 9)):
                            if firstVariantCheck:
                                self.G.remove_edge(*edge3)
                            elif secondVariantCheck:
                                self.G.remove_edge(*edge6)
                        else:
                            if node not in self.throughNodes:
                                self.throughNodes.append(node)
                            if firstVariantCheck:
                                edgesRestore.append(edge)
                                edgesRestore.append(edge2)
                                edgesRestore.append(edge3)
                                if edge3 not in self.throughEdges:
                                    self.throughEdges.append(edge3)
                            else:
                                edgesRestore.append(edge4)
                                edgesRestore.append(edge5)
                                edgesRestore.append(edge6)
                                if edge6 not in self.throughEdges:
                                    self.throughEdges.append(edge6)
                            for edgeNode in self.G.edges(node):
                                self.G.remove_edge(*edgeNode)
                else:
                    try:
                        self.G.remove_edge(*edge3)
                    except:
                        pass
                    try:
                        self.G.remove_edge(*edge6)
                    except:
                        pass

        for edgeR in edgesRestore:
            self.G.add_edge(*edgeR)

        return 1

    def add_edges_to_diagonal_and_through_for_recognition(self):
        for node in self.diagonalNodes:
            i = node[0]
            j = node[1]

            edge = ((i, j), (i + 1, j))
            edge2 = ((i, j), (i, j - 1))
            edge3 = ((i, j), (i, j + 1))
            edge4 = ((i, j), (i - 1, j))

            self.G.add_edge(*edge)
            self.G.add_edge(*edge2)
            self.G.add_edge(*edge3)
            self.G.add_edge(*edge4)

        for node in self.throughNodes:
            i = node[0]
            j = node[1]

            edge = ((i, j), (i + 1, j))
            edge2 = ((i, j), (i, j - 1))
            edge3 = ((i, j), (i, j + 1))
            edge4 = ((i, j), (i - 1, j))

            self.G.add_edge(*edge)
            self.G.add_edge(*edge2)
            self.G.add_edge(*edge3)
            self.G.add_edge(*edge4)

        return 0

    def clean_added_edges(self):
        for node in self.diagonalNodes:
            edges = self.G.edges(node)

            for edge in edges:
                try:
                    self.G.remove_edge(*edge)
                except:
                    pass

        for node in self.throughNodes:
            i = node[0]
            j = node[1]

            edge = ((i, j), (i + 1, j))
            edge2 = ((i, j), (i - 1, j))
            edge3 = ((i, j + 1), (i, j - 1))

            edge4 = ((i, j), (i, j - 1))
            edge5 = ((i, j), (i, j + 1))
            edge6 = ((i - 1, j), (i + 1, j))

            firstVariantCheck = self.check_edge_in_edgelist(
                edge) and self.check_edge_in_edgelist(edge2) and self.check_edge_in_edgelist(edge3)
            secondVariantCheck = self.check_edge_in_edgelist(
                edge4) and self.check_edge_in_edgelist(edge5) and self.check_edge_in_edgelist(edge6)

            try:
                if firstVariantCheck:
                    self.G.remove_edge(*edge4)
                    self.G.remove_edge(*edge5)
                elif secondVariantCheck:
                    self.G.remove_edge(*edge)
                    self.G.remove_edge(*edge2)
            except:
                pass

        return 0

    def get_final_tiles(self, nodeCheck=0, output=True):
        tiles = []

        self.add_edges_to_diagonal_and_through_for_recognition()
        if output:

            for i in range(1, self.n - 1):
                for j in range(1, self.m - 1):
                    node = (i, j)
                    if node in self.throughNodes:
                        print str(node) + ' - tile 5'
                    elif node in self.diagonalNodes:
                        print str(node) + ' - tile 3'
                    elif self.get_simple_degree(node) == 2:
                        print str(node) + ' - tile 1'
                    elif self.get_simple_degree(node) == 3:
                        print str(node) + ' - tile 2'
                    elif self.get_simple_degree(node) == 4:
                        print str(node) + ' - tile 4'

        elif nodeCheck:
            node = nodeCheck
            if node in self.throughNodes:
                tiles.append(5)
            elif node in self.diagonalNodes:
                tiles.append(3)
            elif self.get_simple_degree(node) == 2:
                tiles.append(1)
            elif self.get_simple_degree(node) == 3:
                tiles.append(2)
            elif self.get_simple_degree(node) == 4:
                tiles.append(4)
            else:
                tiles.append(-1)
        else:
            for i in range(1, self.n - 1):
                for j in range(1, self.m - 1):
                    node = (i, j)
                    if node in self.throughNodes:
                        tiles.append(5)
                    elif node in self.diagonalNodes:
                        tiles.append(3)
                    elif self.get_simple_degree(node) == 2:
                        tiles.append(1)
                    elif self.get_simple_degree(node) == 3:
                        tiles.append(2)
                    elif self.get_simple_degree(node) == 4:
                        tiles.append(4)
        self.clean_added_edges()
        return tiles

    def check_excluded(self):
        for node in self.excludedNodes:
            if node in self.excludeDegree.keys():
                if self.G.degree(node) > self.excludeDegree[node]:
                    return 0
            elif self.G.degree(node) > 1:
                return 0
        return 1

    def check_all_tiles_type(self):
        tiles = self.get_final_tiles(output=False)

        if len(set(tiles)) == 5:
            return 1
        else:
            return 0


    def get_tasks(self):

        # Get boundaries
        boundaries = []
        for i in range(self.n - 1):
            boundaries.append((i, 0))
            boundaries.append((i, self.m - 1))
        for j in range(self.m - 1):
            boundaries.append((0, j))
            boundaries.append((self.n - 1, j))
        boundaries.extend(self.excludedNodes)

        series = random.randint(1, 5)

        for i in xrange(series):
            a = random.choice(boundaries)
            b = random.choice(boundaries)
            try:
                bool(nx.shortest_path(self.G, a, b))
                pathExist = ' connected '
            except:
                pathExist = ' not connected '

            print 'Task: ' + str(a) + str(pathExist) + str(b)
        return 1

    def output_graph(self):
        # Graph layout
        pos = {}
        for n in self.G:
            pos[n] = (n[0], n[1])

        # Generate graph image
        edgesWithoutThrough = self.G.edges()
        for edge in self.throughEdges:
            try:
                edgesWithoutThrough.remove((edge[0], edge[1]))
            except:
                pass
            try:
                edgesWithoutThrough.remove((edge[1], edge[0]))
            except:
                pass

        nx.draw_networkx(self.G, pos, edgelist=edgesWithoutThrough)
        nx.draw_networkx(self.G, pos, nodelist=None, edgelist=self.throughEdges, width=2, alpha=0.4, edge_color='b')
        import os

        scriptDir = os.path.dirname(__file__)
        open(os.path.join(scriptDir, 'graph.png'), 'w')
        plt.savefig('graph.png')

        return 1

    def output_image(self):
        import Image


        def get_rotation(node):
            i = node[0]
            j = node[1]

            tile = self.get_final_tiles(nodeCheck=node, output=False)

            edge = ((i, j), (i + 1, j))
            edge2 = ((i, j), (i, j - 1))
            edge3 = ((i, j), (i, j + 1))
            edge4 = ((i, j), (i - 1, j))

            angle = 0
            if tile[0] == 1:
                self.add_edges_to_diagonal_and_through_for_recognition()
                if self.check_edge_in_edgelist(edge) and self.check_edge_in_edgelist(edge2):
                    angle = 0
                elif self.check_edge_in_edgelist(edge) and self.check_edge_in_edgelist(edge3):
                    angle = 90
                elif self.check_edge_in_edgelist(edge3) and self.check_edge_in_edgelist(edge4):
                    angle = 180
                elif self.check_edge_in_edgelist(edge2) and self.check_edge_in_edgelist(edge4):
                    angle = 270

                self.clean_added_edges()
                return angle

            elif tile[0] == 2:
                self.add_edges_to_diagonal_and_through_for_recognition()
                if self.check_edge_in_edgelist(edge) and self.check_edge_in_edgelist(
                        edge2) and self.check_edge_in_edgelist(
                        edge3):
                    angle = 90
                elif self.check_edge_in_edgelist(edge) and self.check_edge_in_edgelist(
                        edge2) and self.check_edge_in_edgelist(edge4):
                    angle = 0
                elif self.check_edge_in_edgelist(edge) and self.check_edge_in_edgelist(
                        edge3) and self.check_edge_in_edgelist(edge4):
                    angle = 180
                elif self.check_edge_in_edgelist(edge3) and self.check_edge_in_edgelist(
                        edge3) and self.check_edge_in_edgelist(edge4):
                    angle = 270

                self.clean_added_edges()
                return angle

            elif tile[0] == 3:
                edge3 = ((i - 1, j), (i, j - 1))
                edge4 = ((i, j + 1), (i + 1, j))

                secondVariantCheck = self.check_edge_in_edgelist(
                    edge3) and self.check_edge_in_edgelist(edge4)

                if secondVariantCheck:
                    angle = 90
            elif tile[0] == 5:
                edge = ((i, j), (i + 1, j))
                edge2 = ((i, j), (i - 1, j))
                edge3 = ((i, j + 1), (i, j - 1))

                firstVariantCheck = self.check_edge_in_edgelist(
                    edge) and self.check_edge_in_edgelist(edge2) and self.check_edge_in_edgelist(edge3)
                if firstVariantCheck:
                    angle = 90

            return angle


        result = Image.new('RGB', (self.n * 170, self.m * 170))

        import os

        scriptDir = os.path.dirname(__file__)

        task = Image.open(os.path.join(scriptDir, 'tiles/task.png'))
        task_object = Image.open(os.path.join(scriptDir, 'tiles/task_object.png'))
        zero = Image.open(os.path.join(scriptDir, 'tiles/0.png'))
        one = Image.open(os.path.join(scriptDir, 'tiles/1.png'))
        two = Image.open(os.path.join(scriptDir, 'tiles/2.png'))
        three = Image.open(os.path.join(scriptDir, 'tiles/3.png'))
        four = Image.open(os.path.join(scriptDir, 'tiles/4.png'))
        five = Image.open(os.path.join(scriptDir, 'tiles/5.png'))

        for i in (xrange(self.n)):
            for j in (xrange(self.m)):
                node = (i, j)

                width = i * 170
                height = (self.m - j - 1) * 170

                tiles = self.get_final_tiles(nodeCheck=node, output=False)
                if node in self.excludeDegree:
                    if tiles[0] == 0:
                        result.paste(zero, (width, height))
                    else:
                        if random.random() >= 0.5:
                            self.taskObjects[node] = 'a'
                            result.paste(task, (width, height))
                        else:
                            self.taskObjects[node] = 'b'
                            result.paste(task_object, (width, height))
                elif tiles[0] == 0:
                    result.paste(zero, (width, height))
                elif tiles[0] == 1:
                    result.paste(one.rotate(get_rotation(node)), (width, height))
                elif tiles[0] == 2:
                    result.paste(two.rotate(get_rotation(node)), (width, height))
                elif tiles[0] == 3:
                    result.paste(three.rotate(get_rotation(node)), (width, height))
                elif tiles[0] == 4:
                    result.paste(four, (width, height))
                elif tiles[0] == 5:
                    result.paste(five.rotate(get_rotation(node)), (width, height))
                elif self.G.degree(node) == 0:
                    result.paste(zero, (width, height))
                elif node not in self.G.nodes():
                    result.paste(zero, (width, height))
                else:
                    if random.random() >= 0.5:
                        self.taskObjects[node] = 'a'
                        result.paste(task, (width, height))
                    else:
                        self.taskObjects[node] = 'b'
                        result.paste(task_object, (width, height))
        # result.format = "PNG"
        # result.show()
        # open(os.path.join(scriptDir, 'tile.png'), 'w')
        result.save(os.path.join(scriptDir, 'tile.png'), 'PNG')
        pass

    def export_plist(self):
        import plistlib

        plist = dict()
        plist['Tiles'] = [0, 1, 2, 3, 4]

        tiles = self.get_final_tiles(output=False)
        plist['TilesCount'] = dict((str(i), tiles.count(i)) for i in tiles)

        plist['Solutions'] = [{'Positions': tiles}]

        plistlib.writePlist(plist, 'output.plist')

        return 1

    def make_map(self):
        checkExclude = False
        checkTilesType = False
        while not (checkTilesType and checkExclude):
            self.generate_full_connected_grid()
            self.randomize_removing_edges()
            self.remade_network_by_tile()
            checkExclude = self.check_excluded()
            if self.allTileTypes:
                checkTilesType = self.check_all_tiles_type()
            else:
                checkTilesType = True

        self.get_final_tiles()
        self.get_tasks()
        self.export_plist()
        self.output_image()
        self.output_graph()
        # print self.taskObjects


# exclude = [(2, 4), (2, 3), (3, 3)]
exclude = []
# for i in xrange(6, 9):
#     for j in xrange(1, 6):
#         node = (i, j)
#         exclude.append(node)
#
# for i in xrange(1, 4):
#     for j in xrange(6, 11):
#         node = (i, j)
#         exclude.append(node)
#
# triangleLeft = [(1, 1), (1, 2), (1, 3), (1, 4), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (4, 1)]
# triangleRight = [(8, 10), (8, 9), (8, 8), (8, 7), (7, 10), (7, 9), (7, 8), (6, 10), (6, 9), (5, 10)]
# exclude.extend(triangleLeft)
# exclude.extend(triangleRight)

# exclude.extend([(3, 3), (5, 5)])
excludeNodeWithDegree = {}
# excludeNodeWithDegree[(2, 3)] = 2
# excludeNodeWithDegree[(3, 4)] = 2
# print excludeNodeWithDegree

map = GameMap(5, 5, difficultCoefficient=0.2, exclude=exclude, allTileTypes=True, excludeDegree=excludeNodeWithDegree)
map.make_map()
