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
        for currentX in range(0,dimension):
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
        length, _ = dimension
        numberOfQuadrants = 2**orderOfCurve
        # TODO: Add an int() to assess its impact on the quotieint
        threshold = length / numberOfQuadrants
        return threshold

    def buildHilbertSolution(self,straightLinePath,start,goal,foundVertices,length,orderOfCurve,variances,dimension,current = None):
        # Getting the threshold for the current Hilbert curve
        threshold = self.determineLocalSweep(length,orderOfCurve,dimension)
        # Getting the orientation to goal's coordinate
        goalOrientation = self.orientationToGoal(start,goal)

        """Decision making step."""
        # Since a straight line is the closest path between two points ,we will use it
        # as a guide and whenever we night to go off path, the Hilbert Vertices with 
        # anchor our region of exploration.
        currentVertex = start
        currentNode = LinkedListNode(currentVertex)
        generatedPath = DoublyLinkedList(currentNode)
        generatedPath.updateLength()
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
                generatedPath.updateLength()
                currentVertex = nextVertex
                currentNode = nextNode
                vertexIndex += 1
            # Straight line vertex is not in free space/ freeSpaceGraph
            else:
                vertex = self.getInteger(vertex)
                nearestNeighbours = self.getNearestNeighbours(foundVertices,vertex,threshold,variances,goalOrientation,dimension,straightLinePath)
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


    def localPlanner(self,currentNode,localStart,target,isOptimal):
        # TODO: Might need to get rid of all of the lines beofre currentVertex
        # Calculate the slope
        slope = None
        # Generate the straight line approximate solution
        straightLinePath = None
        # Calculate the orientation to goal
        orientationToGoal = self.orientationToGoal(localStart,target)
        # Obtain the peek directions
        peekDirection = self.peekDirectionsToTarget(orientationToGoal)
        # Traverse the straight line 
        currentVertex = localStart
        vertex = currentVertex
        vertexIndex = 0
        straightPath = straightLinePath.keys()
        while vertex != target:
            # TODO: We need some flag that will indicate whether we reinitialize
            # the vertex index since we're building a new straight line or whether we're traversing the 
            # current straight line to the target ( No obstacle on path).
            # Calculate the slope
            slope = None
            # Generate the straight line approximate solution
            straightLinePath = None
            # Calculate the orientation to goal
            orientationToGoal = self.orientationToGoal(vertex,target)
            # Obtain the peek directions
            peekDirection = self.peekDirectionsToTarget(orientationToGoal)
            vertex = straightPath[vertexIndex]
            if straightLinePath[vertex]:
                if vertex == localStart:
                    vertexIndex += 1
                # The vertex in straightLine is in free space
                nextNode = self.makeLocalConnection(currentNode,vertex)
                currentVertex = vertex
                currentNode = nextNode
                vertexIndex += 1
            else: # Not in free space
                for direction in peekDirection:
                    vertexInteger = self.getInteger(vertex)
                    xPeek = vertexInteger[0] + direction[0]
                    yPeek = vertexInteger[1] + direction[1]

                    stringXYPeek = self.getStringKeys(xPeek,yPeek)
                    if stringXYPeek in self.freeSpaceGraph:
                        nextNode = self.makeLocalConnection(currentNode,stringXYPeek)
                        currentVertex = stringXYPeek
                        currentNode = nextNode
                        continue
        # This will be the tail node and we can traverse it in the reverse direction
        return currentNode
            



    def getNearestNeighbours(self,foundHilberts,currentVertex,threshold,varianceConstant,goalOrientation,dimension,straightLine=None):
        # TODO: WE NEED TO BIAS THE THRESHOLD AND VARIANCE IN THE DIRECTION OF THE GOAL.
        possibleHilbertOffsets = self.getVerticesFromThreshold(threshold)
        nearestNeighbours = set()
        for offset in possibleHilbertOffsets:
            #nearestNeighbours = []
            xCandidate = currentVertex[0] + offset[0]
            xCandidate = self.roundValue(xCandidate)
            yCandidate = currentVertex[1] + offset[1]
            yCandidate = self.roundValue(yCandidate)
            if self.notInRange(xCandidate,yCandidate,dimension):
                continue
            hilbertCandidate = self.getStringKeys(xCandidate,yCandidate)
            # The candidate if on a valid hilbert vertex
            # TODO: This has to be a bit more sophisticated. Maybe look if a hilbert curve is a pixel away from a possible hilbert vertex
            if hilbertCandidate in foundHilberts:
                if foundHilberts[hilbertCandidate]:
                    # Whenever we find a neighbour we append and move on
                    nearestNeighbours.add([xCandidate,yCandidate])
                    continue
            else:
                # We apply variances to attempt to get a solution
                variances = self.applyVariances(varianceConstant,[xCandidate,yCandidate])
                for variancePoint in variances:
                    # TODO: Modified the logic here
                    # XVarCandidate = xCandidate + variance[0]
                    # yVarCandidate = yCandidate + variance[1]
                    # Check if varinace candidate is valid
                    varinceCandidateKey = self.getStringKeys(variancePoint[0],variancePoint[1])
                    # If we find the variance vertex in hilbert space we add it to neighbours
                    # and we move on.
                    if varinceCandidateKey in foundHilberts:# or varinceCandidateKey in self.freeSpaceGraph:
                        # nearestNeighbours.add(variancePoint)
                        nearestNeighbours.add(varinceCandidateKey)
                        break
        return nearestNeighbours


    def getVerticesFromThreshold(self,thresholdValue):
        """Append optimal node varinaces first."""
        offests = [[thresholdValue,0],
                   [thresholdValue,-thresholdValue],
                   [0,-thresholdValue],
                   [-thresholdValue,-thresholdValue],
                   [-thresholdValue,0],
                   [-thresholdValue,thresholdValue],
                   [0,thresholdValue],
                   [thresholdValue,-thresholdValue]]
        return offests
    

    def getInteger(self,vertex):
        """Return the integer value of the current vertex."""
        coordinates = vertex.split(",")
        coordinates[0] = int(coordinates[0])
        coordinates[1] = int(coordinates[1])
        return coordinates
    
    def roundValue(self,value):
        if isinstance(value,int):
            pass
        else:
            stringValue = str(value)
            partitioned = stringValue.split(".")
            # print(partitioned[1])
            intDecimal = int(partitioned[1])
            if intDecimal >= 50:
                value = int(partitioned[0]) + 1
            else:
                value = int(partitioned[0])
        return value
    
    def orientationToGoal(self,start,goal):
        """Helper function to determine the direction in which the goal configuration lies
        relative to the start configuration."""
        x1, y1 = start
        x2, y2 = goal

        if x1 > x2:
            horizontalDirection = 'L'
        elif x1 < x2:
            horizontalDirection = 'R'
        else:
            horizontalDirection = '_'

        if y1 > y2:
            verticalDirection = 'U'
        elif y1 < y2:
            verticalDirection = 'D'
        else:
            verticalDirection = '_'
        return horizontalDirection + verticalDirection

    def notInRange(self,x,y,dimension):
        return (0>=x and x<dimension[0]) and (0>=y and y<dimension[1])

    def peekDirectionsToTarget(self,orientationToGoal):
        if orientationToGoal == "R_":
            return [[1,-1],[1,1]]
        if orientationToGoal == "RU":
            return [[1,0],[0,-1]]
        if orientationToGoal == "_U":
            return [[1,-1],[-1,-1]]
        if orientationToGoal == "LU":
            return [[0,-1],[-1,0]]
        if orientationToGoal == "L_":
            return [[-1,-1],[-1,1]]
        if orientationToGoal == "LD":
            return [[-1,0],[0,1]]
        if orientationToGoal == "_D":
            return [[-1,1],[1,1]]
        if orientationToGoal == "RD":
            return [[0,1],[1,0]]
    
    def makeLocalConnection(self,currentNode,nextVertex):
        nextNode = LinkedListNode(nextVertex)
        currentNode.next = nextNode
        nextNode.prev = currentNode
        return nextNode
        
    def getStringKeys(self,x,y):
        return str(x) + "," + str(y)
    
    def applyVariances(self,varianceConstant,candidate):
        variancePoints = [[varianceConstant,0],
                          [varianceConstant,-varianceConstant],
                          [0,-varianceConstant],
                          [-varianceConstant,-varianceConstant],
                          [-varianceConstant,0],
                          [-varianceConstant,varianceConstant],
                          [0,varianceConstant],
                          [varianceConstant,varianceConstant]]
        hilbertVaried = []
        for var in variancePoints:
            hilbertVaried.append([candidate[0]+var[0],candidate[1]+var[1]])
        return hilbertVaried
    
    def displayPath(self,linkedList):
        current = linkedList
        while current is not None:
            print(current.value)
            print('|')
            print('V')
            current = current.next

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
        self.length = 0

    def updateLength(self):
        self.length += 1
"""
myAnchor = Anchor({},{},(0,0),(82,50))
print(myAnchor.slope)
print(myAnchor.yIntercept)
print(myAnchor.equationOfLineOutput(33))
print(myAnchor.equationOfLineOutput(50))
print(myAnchor.equationOfLineOutput(82))
line = myAnchor.generateStraightLineCoordinates(100)
"""