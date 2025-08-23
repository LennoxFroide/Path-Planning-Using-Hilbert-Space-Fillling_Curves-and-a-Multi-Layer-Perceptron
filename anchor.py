class Anchor:
    def __init__(self,foundVerticesMap,freeSpaceGraph,XStart,XGoal):
        self.hilbertVertices = foundVerticesMap
        self.freeSpaceGraph = freeSpaceGraph
        self.start = XStart
        self.goal = XGoal
        self.slope, self.yIntercept = self.getSlopeAndYIntercept()
        # TODO: Have to reinitialize to look like class properties that are initialized in other functions
        self.path = None

    def getSlopeAndYIntercept(self):
        """Helper function to determine the slope of the straight line connecting
        the start coordinate and the goal coordinate."""
        x1, y1 = self.start
        x2,y2 = self.goal

        slope = (y2 - y1) / (x2 - x1)
        # Getting the y-intercept; the value of x must be 0
        c = y2 - slope*(x2)
        ctest = y1 - slope*(x1)
        if c != ctest:
            raise Exception("Error in calculating the y-intercept")
        return (slope,c)
    
    def equationOfLineOutput(self,currentX):
        """Helper function that uses the equation of a line to return the corresponding
        y value to any x value that it is supplied with."""
        matchingYValue = self.slope * currentX + self.yIntercept
        return matchingYValue
    
    def generateStraightLineCoordinates(self,dimension): # O(N) Time might be unnecessary
        """Helper function that generates al of the (x,y) pairs that lie on a straight 
        line connecting start coordinate"""
        straightLineCoordinatesMap = dict()
        for currentX in range(0,dimension + 1):
            currentY = int(self.equationOfLineOutput(currentX))
            stringCoordinate = self.getStringKeys(currentX,currentY)
            straightLineCoordinatesMap[stringCoordinate] = False
        return straightLineCoordinatesMap

    def getStraightLineVerticesInFreeSpace(self,lineCoordinates,freeSpaceGraph):
        """Helper function to identify the vertices of the straight line that fall in the 
        ffreespace of the occupancy map."""
        for stringKey, _ in lineCoordinates.items():
            if stringKey in freeSpaceGraph:
                lineCoordinates[stringKey] = True
        return lineCoordinates
    
    def determineLocalSweep(self,length,orderOfCurve,dimension):
        length = dimension
        numberOfQuadrants = 2**orderOfCurve
        # TODO: Add an int() to assess its impact on the quotieint
        threshold = length / numberOfQuadrants
        return threshold

    def buildHilbertSolution(self,straightLinePath,start,goal,foundVertices,length,orderOfCurve,dimension,current = None):
        # Getting the threshold for the current Hilbert curve
        threshold = self.determineLocalSweep(length,orderOfCurve,dimension)
        # Getting the orientation to goal's coordinate
        goalOrientation, variances = self.orientationToGoal(start,goal)

        """Decision making step."""
        # Since a straight line is the closest path between two points ,we will use it
        # as a guide and whenever we night to go off path, the Hilbert Vertices with 
        # anchor our region of exploration.
        currentVertex = start
        currentNode = LinkedListNode(currentVertex)
        generatedPath = DoublyLinkedList(currentNode)
        # currentPointer = currentNode
        # Traversing the straight line path
        straightLineVertices = list(straightLinePath.keys())
        vertexIndex = 0
        while vertexIndex < len(straightLineVertices):
            vertex = straightLineVertices[vertexIndex]
            value = straightLinePath[vertex]
            if value == True:# Purely straight line points connections
                nextVertex = vertex
                nextNode = self.makeLocalConnection(currentNode,nextVertex)
                currentVertex = nextVertex
                currentNode = nextNode
                vertexIndex += 1
            # Straight line vertex is not in free space/ freeSpaceGraph
            else:
                nearestNeighbours = self.getNearestNeighbours(foundVertices,vertex,threshold,variances,goalOrientation,straightLinePath)
                currentVertexInteger = self.getInteger(currentVertex)
                optimalPoint = [currentVertexInteger[0] + threshold, currentVertexInteger[1] + threshold]
                optimalPointString = self.getStringKeys(optimalPoint)
                if optimalPoint in foundVertices or optimalPoint in straightLinePath: # or optimalPoint in self.freeSpaceGraph:
                    nextVertex = optimalPoint
                    endNodeAtOptimal = self.localPlanner(currentVertex,optimalPoint,True)
                    # Need to override the for loop
                    while True:
                        vertex = straightLineVertices[vertexIndex]
                        if not straightLinePath[vertex]:
                            vertexIndex += 1
                            """
                            nextStraightLineVertex = self.getInteger(vertex)
                            break
                            """
                        else:
                            nextStraightLineVertex = self.getInteger(vertex)
                            break
                            # vertexIndex += 1
                    endNodeBackAtStraightLine = self.localPlanner(optimalPoint,nextStraightLineVertex,False)
                    currentVertex = nextStraightLineVertex
                    vertexIndex += 1
                else:# Optimal point is not found
                    # We need to iterate all of the nearest neighbours
                    # Use the manhattan distance to determine the closest neighbour 
                    # Then build a path to the neighbour from currentVertex to nearest neighbour
                    # Then from nearest neighbour to the next straightline vertex
                    pass
        return generatedPath


    def localPlanner(self,start,end,isOptimal):

        pass



    def getNearestNeighbours(self,foundHilberts,currentVertex,threshold,variances,goalOrientation,straightLine=None):
        possibleHilbertOffsets = self.getVerticesFromThreshold(threshold,goalOrientation)
        nearestNeighbours = set()
        for offset in possibleHilbertOffsets:
            #nearestNeighbours = []
            xCandidate = currentVertex[0] + offset[0]
            yCandidate = currentVertex[1] + offset[1]
            if self.notInRange(xCandidate,yCandidate):
                continue
            hilbertCandidate = self.getStringKeys(xCandidate,yCandidate)
            # The candidate if on a valid hilbert vertex
            if hilbertCandidate in foundHilberts:
                if foundHilberts[hilbertCandidate]:
                    # Whenever we find a neighbour we append and move on
                    nearestNeighbours.add([xCandidate,yCandidate])
                    continue
                else:
                    # We apply variances to attempt to get a solution
                    for variance in variances:
                        XVarCandidate = xCandidate + variance[0]
                        yVarCandidate = yCandidate + variance[1]
                        # Check if varinace candidate is valid
                        varinceCandidateKey = self.getStringKeys(XVarCandidate,yVarCandidate)
                        # If we find the variance vertex in hilbert space we add it to neighbours
                        # and we move on.
                        if varinceCandidateKey in foundHilberts or varinceCandidateKey in self.freeSpaceGraph:
                            nearestNeighbours.add([XVarCandidate,yVarCandidate])
                            break
        return nearestNeighbours

        pass
    def getVerticesFromThreshold(self,thresholdValue,goalOrientation):
        """Append optimal node varinaces first."""
        pass

    def getInteger(self,vertex):
        """Return the integer value of the current vertex."""
        pass

    def orientationToGoal(self,start,goal):
        pass

    def notInRange(self,x,y):
        pass

    def makeLocalConnection(self,currentNode,nextVertex):
        nextNode = LinkedListNode(nextVertex)
        currentNode.next = nextNode
        nextNode.prev = currentNode
        return nextNode
        
    def getStringKeys(self,x,y):
        return str(x) + "," + str(y)

class LinkedListNode:
    """Class defining the properties of the nodes that form the final solution."""
    def __init__(self,vertex):
        self.value = vertex
        self.prev = None
        self.next = None

class DoublyLinkedList:
    """The entire path/solution from head node to tail node."""
    def __init__(self,node):
        self.head = node
        self.tail = None
"""
myAnchor = Anchor({},{},(0,0),(82,50))
print(myAnchor.slope)
print(myAnchor.yIntercept)
print(myAnchor.equationOfLineOutput(33))
print(myAnchor.equationOfLineOutput(50))
print(myAnchor.equationOfLineOutput(82))
line = myAnchor.generateStraightLineCoordinates(100)
"""