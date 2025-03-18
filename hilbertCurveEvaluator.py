def assesCurveValidity(foundVertices):
    """This function will return valid if the order of the 
    Hilbert Curve generated will successfully get us from the start 
    configuration to the goal configuration."""
    VALID = False
    # We will obtain all of the keys of the graph and iterate them using a fixed window
    vertices = foundVertices.keys()
     # Calculating total points
    totalPoints = len(vertices)
    # Getting the set of points that meet the threshold
    threshold = int(0.75*totalPoints)
    # Iterating
    firstPairIdx = 0
    # The first vertex will go up until before last vertex in the list
    while firstPairIdx < totalPoints - 2:
        # currentlyValid = False
        # getting the 2nd pair
        secondPairIdx = firstPairIdx + 1
        # Grabbing the values of the pair
        firstPairValue = foundVertices[vertices[firstPairIdx]]
        secondPairValue = foundVertices[vertices[secondPairIdx]]
        # We have found both vertices within free space (CFREE)
        if firstPairValue and secondPairValue or firstPairValue or secondPairValue:
            # currentlyValid = True
            threshold = evaluateThreshold(firstPairValue, secondPairValue)
        firstVertex += 2
    return threshold == 0

def evaluateThreshold(firstCoordinate, secondCoordinate,thershold):
    """This function will evaluate whether or not the current order
    of the Hilbert curve meets the set threshold for it to be a valid
    probabilistic roadmap(very dense  roadmap)."""
    # For a point to be a threshold point it has to lie in:
    # 1.) REGION 1 -> X => [0,50], Y => [0,50]
    #                  OR
    # 2.) REGION 2 -> X =>[0,100], Y =>[50,100]
    firstPairCoord = getXYCoordinate(firstCoordinate)
    secondPairCoord = getXYCoordinate(secondCoordinate)
    if pairInRegionOneOrTwo([firstPairCoord,secondPairCoord]):
        thershold -= 1
    return thershold


def pairInRegionOneOrTwo(coordinateSet):
    """This function checks whether the hilbert curve vertices found in the 
    free space subset of Cspace are priority points"""
    # Checking for region 1
    inRegionOne = False
    inRegionTwo = False
    for coordinate in coordinateSet:
        xValue, yValue = coordinate
        if xValue >= 0 and xValue <= 50 and yValue >= 0 and yValue <= 50:
            inRegionOne = True
        elif xValue >= 0 and xValue <= 99 and yValue >= 50 and yValue <= 99:
            inRegionTwo = True
    return inRegionOne or inRegionTwo




def getXYCoordinate(firstCoordinate):
    """This function takes in a string coordinate and returns a set of intergers
    x-y pair."""
    # Converting the string into an integer
    stringDigits = firstCoordinate.strip(',')
    # Generating list of xy pair as string list elements
    xySet = stringDigits.split()
    # Converting the string pair into integers
    xySet[0] = int(xySet[0])
    xySet[1] = int(xySet[1])
    return xySet