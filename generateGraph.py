import numpy as np
VISITED = True
# We will use the Boogle Board algorithm to generate the graphs
def getRandomPoints(array):
    """ This helper function will generated 3 random points
    from the gaussian distribution around out vertices.
    The generated points will be joined to form a graph."""
    randomNode = []
    for vertex in array:
        randomPoints = []
        randomPoints.append(np.random.normal(loc=vertex, scale=0.01))
        randomPoints.append(np.random.normal(loc=vertex, scale=0.01))
        randomNode.append(randomPoints)

def generateFreeSpace(occupancyMatrix):
    # A dictionary to store the vertices and their neighbours
    freeSpaceGraph = {}
    # Indices of possible neighbours
    #                   LEFT   RIGHT BOTTOM  TOP  TOP-LEFT TOP-RIGHT BOTTOM_LEFT BOTTOM-RIGHT
    neighbourIndices = [[0,-1],[0,1],[-1,0],[1,0],[1,-1],[1,1],[-1,-1],[-1,1]]
    # Iterating the occupancy map
    for row in range(len(occupancyMatrix)):
        for column in range(len(occupancyMatrix[row])):
            # Checking whether we have an obstacle or the position has been visited
            currentElement = occupancyMatrix[row][column]
            # We will skip such elements
            if currentElement == VISITED or currentElement == 1:
                continue
            # We are at a free space and we need to visit this node
            neighboours = getNeighbours(row, column, neighbourIndices, occupancyMatrix)
    
            pass
    return neighboours
    
def getNeighbours(row, column, neighbourIndices, matrix):
    neighbours = []
    # Iterating all of the possible indices
    for index in neighbourIndices:
        # Generating the current index
        currentRow, currentColumn = row + index[0], column + index[1]
        if currentRow > 0 and currentRow < len(matrix):
            if currentColumn > 0 and currentColumn < len(matrix[row]):
                neighbours.append([currentRow,currentColumn])

    return neighbours
    """
    # Grabbing neighbour from left and right first
    if column > 0 and column < len(matrix[row]):
        # We have a valid left neighbour
    """
    pass