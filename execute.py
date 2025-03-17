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

##---------------------------VARIABLES NEEDED TO RUN HILBERT-CURVE-RELATED MODULE FUNCTIONS--------------------------------------##
# Order of the curve
ORDER = 4
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
##---------------------------VARIABLES NEEDED TO RUN OCCUPANCY MAP AND FREE SPACE RELATED MODULE FUNCTIONS-------------------------##
# # RESOLUTION
# RESOLUTION = (100,100)
def wait():
    for i in range(100):
        pass

# TODO: 1. Create a Hilbert Curve
path = hilbGen.pathPlanner(PATH,ORDER,RESOLUTION) 
"""Randomizing the vertices"""
nodes = getRand.getRandomPoints(path)
"""Plotting the hilbert curve vertices"""
hilbGen.drawHilbert(RESOLUTION,path) 
hilbGen.drawHilbertRand(RESOLUTION,nodes)

# TODO: 2. Generate a graph holding Hilbert curve vertices
hilbertGraph = gt.generateGraph(nodes,HILBERT_GRAPH)
print(hilbertGraph)

# TODO: 3. Create an occupancy map
generatedMaps = occupyGen.generateOccupancyMap(RESOLUTION) 
# print(generatedMaps[1])
occupyGen.occupanyMapPlotter(generatedMaps)

# TODO: 4. Convert occupancy map into a graph of Cfree nodes
freeSpaceGraph = getRand.generateFreeSpace(generatedMaps[3])
# print(freeSpaceGraph)
# TODO: 5. Traverse the graph of Cfree and search for the Hilbert vertices in it
hilbertFound = traverse.getVertices(freeSpaceGraph,hilbertGraph)
wait()
