def getLength(array):
    """Helper function to print the number of vertex pair"""
    return len(array)


def generateGraph(matrix,HILBERT_GRAPH):
    """Helper function to generate the graph from Hilbert vertices"""
    # A set of (x,y) pairs
    # matrix[idx][0], matrix[idx][1]
    # hilbertGraph = {}
    # Start node matrix[0][0] -> matrix[0][1]
    for row in range(len(matrix) - 1):
        # for column in range(len(matrix[row])):
        column = 0
        firstX, firstY = matrix[row][column]
        firstKey = getHilbertGraphKeys(firstX, firstY)
        HILBERT_GRAPH[firstKey] = [int(matrix[row][column + 1][0]),int(matrix[row][column + 1][1])]
        secondX, secondY = matrix[row][column + 1]
        secondKey = getHilbertGraphKeys(secondX, secondY)
        HILBERT_GRAPH[secondKey] =  [int(matrix[row + 1][column][0]),int(matrix[row + 1][column][1])]
    lastX, lastY = matrix[-1][0]
    lastKey = getHilbertGraphKeys(lastX,lastY)
    HILBERT_GRAPH[lastKey] = [int(matrix[-1][1][0]),int(matrix[-1][1][1])]
    return HILBERT_GRAPH

def getHilbertGraphKeys(firstCoordinate, secondCoordinate):
    return str(int(firstCoordinate)) + ',' + str(int(secondCoordinate))
