import numpy as np
# Module that generates the Hilbert curve
import hilbertGenerator as hilbGen
# Module that converts hilbert curve vertices into a graph
import generateHilbertGraph as gt
# Module generating occupany map
import occupancyMapGen as occupyGen
# Module that converts the configuration space into CFree(obstacle-free points in Cspace) graph
import generateGraph as getRand
# Module with functions that traverse the free space graph and search for hilbert curve vertices
import graphTraversal as traverse
# Module to evaluate whether or not the current order HCurve is a valid roadmap
import hilbertCurveEvaluator as hcEvaluator

##---------------------------VARIABLES NEEDED TO RUN HILBERT-CURVE-RELATED MODULE FUNCTIONS--------------------------------------##
# Order of the curve
ORDERS = [3,4,5,6]
"""
# Number of quadrants required for this order HC curve
QUADRANTS = 2 ** ORDER
# Total number of vertices
TOTAL_VERTICES = QUADRANTS*QUADRANTS
# PATH
PATH = [None] * TOTAL_VERTICES
# Hilbert Graphs
HILBERT_GRAPH = {}
# RESOLUTION
RESOLUTION = (100,100)
"""
# TODO: GENERATE A SET OF OCCUPANCY MAPS AND PUT EACH ONE THROUGH THIS AUTOMATED PROCESS
##---------------------------VARIABLES NEEDED TO RUN OCCUPANCY MAP AND FREE SPACE RELATED MODULE FUNCTIONS-------------------------##
# # RESOLUTION
# RESOLUTION = (100,100)
# VALID = None
def wait():
    for i in range(100):
        pass
#RESOLUTION = (100,100)
# TODO: 3. Create an occupancy map
# generatedMaps = occupyGen.generateOccupancyMap(RESOLUTION) 
# print(generatedMaps[1])
# VALID = None
hitAppend = 0
hitValid = 0
#occupyGen.occupanyMapPlotter(generatedMaps)
def execute(generatedMaps,labelsNpArray):
    # TODO: Delete these two counters
    hitAppend = 0
    hitValid = 0
    generatedLabels = []
    RESOLUTION = (100,100)
    VALID = None
    mapToIterate = len(generatedMaps)
    for mapIdx in range(1,mapToIterate + 1):
        print(f'Going into map {mapIdx}. \n\n')
        print(f'Old map had valid HC of order {VALID} \n\n')
        VALID = None
        baseRemainingThresholdRatio = None
        # TODO: 4. Convert occupancy map into a graph of Cfree nodes
        freeSpaceGraph = getRand.generateFreeSpace(generatedMaps[mapIdx])
        for ORDER in ORDERS:
            didBreak = False
            # Number of quadrants required for this order HC curve
            QUADRANTS = 2 ** ORDER
            # Total number of vertices
            TOTAL_VERTICES = QUADRANTS*QUADRANTS
            # PATH
            PATH = [None] * TOTAL_VERTICES
            # Hilbert Graphs
            HILBERT_GRAPH = {}
            # RESOLUTION
            RESOLUTION = (100,100)
            # TODO: 1. Create a Hilbert Curve
            path = hilbGen.pathPlanner(PATH,ORDER,RESOLUTION) 
            """Randomizing the vertices"""
            nodes = getRand.getRandomPoints(path)
            """Plotting the hilbert curve vertices"""
            # hilbGen.drawHilbert(RESOLUTION,path) 
            # hilbGen.drawHilbertRand(RESOLUTION,nodes)

            # TODO: 2. Generate a graph holding Hilbert curve vertices
            hilbertGraph = gt.generateGraph(nodes,HILBERT_GRAPH)
            # print(hilbertGraph)

            # TODO: 3. Create an occupancy map
            # generatedMaps = occupyGen.generateOccupancyMap(RESOLUTION) 
            # print(generatedMaps[1])
            # occupyGen.occupanyMapPlotter(generatedMaps)

            # TODO: 4. Convert occupancy map into a graph of Cfree nodes
            # freeSpaceGraph = getRand.generateFreeSpace(generatedMaps[1])
            # print(freeSpaceGraph)
            # TODO: 5. Traverse the graph of Cfree and search for the Hilbert vertices in it
            hilbertFound = traverse.getVertices(freeSpaceGraph,hilbertGraph)
            # TODO: 6. Evaluate whether this is a valid curve
            isValid,remainingThresholdPointsRatio = hcEvaluator.assesCurveValidity(hilbertFound[0])
            if isValid:
                hitValid+= 1
                print(f'hit valid: {hitValid}')
                VALID = ORDER
                baseRemainingThresholdRatio = 2
                print(f'Best Optimal path is along Hilbert Curve of order: {ORDER}')
                # Allow oversampling
                continue
            else:
                if ORDER == 3: # Setting our base threshold ration
                    baseRemainingThresholdRatio = remainingThresholdPointsRatio
                    VALID = ORDER
                    continue
                elif remainingThresholdPointsRatio <= baseRemainingThresholdRatio + 1:# Evaluating the new ratio
                    # Updating threshold in case we have a new best value/ to make our bounds tighter
                    baseRemainingThresholdRatio = min(remainingThresholdPointsRatio,baseRemainingThresholdRatio)
                    VALID = ORDER
                    continue
                else:
                    VALID = ORDER
                    generatedLabels.append(VALID)
                    hitAppend += 1
                    print(f'hit append: {hitAppend}')
                    print(f'Optimal path is along Hilbert Curve of order: {VALID}')
                    # We will turn the valid order of hilbert curve into a numpy array and then append this array
                    # labelsNpArray = np.append(labelsNpArray,np.array(VALID))
                    didBreak = True
                    break
        # If all of the hilbert curves are iterated successfully
        # the algorithm will not break and we therefore have to store the label before 
        # progressing to the next occupancy map
        if not didBreak:# Handles edge case
            generatedLabels.append(VALID)
    labelsNpArray = updateLabelsNpArray(labelsNpArray,generatedLabels)
    return labelsNpArray

def updateLabelsNpArray(labelsNpArray,generatedLabels):
    dummyNpArray = np.zeros((1))
    dummyNpArray[0] = None
    """This function will take the labels used to classify each occupancy map
    and convert them into np arrays and then save then in the set labels array."""
    for label in generatedLabels:
        arrayLabel = np.zeros((1))
        # Convert label into numpy array
        arrayLabel[0] = label
        # Adding the label to the set label array
        dummyNpArray = np.append(dummyNpArray,arrayLabel, axis = 0)
    labelsNpArray = dummyNpArray[1:]
    return labelsNpArray

                