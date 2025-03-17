def getVertices(freeSpaceGraph, hilbertVertexGraph):
    """Module that creates data structures to keep track of the HC vertices
    that were found in free space graph. It also calls the function that 
    performs a depth first search on the free space graph."""
    # Map to keep track of hilbert curve vertices found in free space
    foundVert = {}
    # Generating a set of all hilbert cuvre vertices
    vertexSet = hilbertVertexGraph.keys()
    # Adding the hilbert graph vertices as keys. This map will be
    # updates whenever we find a hilbert curve vertex in free space
    for hilbertVertex in vertexSet:
        foundVert[hilbertVertex] = False
    # Map to keep track of the nodes in the free space graph that we
    # have already visited
    visitedNodes = {}
    # The X_START in CSPACE will always be at coordinate (0,0)
    # xStart = '0,0' #--> Always assume that this 
    # Grabbing the first vertex on the free space graph
    # firstVertex = freeSpaceGraph[xStart]
    firstNode = getFirstNode(freeSpaceGraph)
    # firstVertex = list(next(iter(freeSpaceGraph).strip(',')))
    # Generating a string version of the vertex
    # strFirstVertex = getStringKey(firstVertex[0],firstVertex[1])
    # Grabbing the neighbours of this node
    nodesList = freeSpaceGraph[firstNode]
    # Iterating the paths starting from these nodes
    for node in nodesList:
        nodeString = getStringKey(node[0],node[1])
        # If node has been visited then we skip it
        if nodeString in visitedNodes:
            continue
        # Performing depth first search on the free space graph
        searchCurveVertices(freeSpaceGraph,nodeString,visitedNodes,foundVert)
    return [foundVert,visitedNodes]


def getStringKey(x,y):
    return str(x) + ',' + str(y)

def searchCurveVertices(freeSpaceGraph,node,visitedMap,foundVertices):
    """Function that performs a depth first search on the free space
    graph and looks for hilbert curve vertices."""
    # We start by marking the node as visited
    visitedMap[node] = True
    # We check if this node is a vertex on the hilbert curve
    if node in foundVertices:
        foundVertices[node] = True
    # Grabbing this nodes neighbours
    neighbours = freeSpaceGraph[node]
    # Performing depth first search on the node's neighbours
    for neighbour in neighbours:
        strNeighbour = getStringKey(neighbour[0],neighbour[1])
        # This keeps up from performing repeat work
        if strNeighbour in visitedMap:
            continue
        else:
            searchCurveVertices(freeSpaceGraph,strNeighbour,visitedMap,foundVertices)

    return

def getFirstNode(freeSpaceGraph):
    """This function will get the first node that has neighbours in the free
    space graph after node (0,0)"""
    # Converting keys into a list
    nodeKeys = freeSpaceGraph.keys()
    for nodeKey in nodeKeys:
        # Grabbing the first node that has neighbours
        currNeighbourCount = len(freeSpaceGraph[nodeKey])
        if currNeighbourCount > 0:
            return nodeKey