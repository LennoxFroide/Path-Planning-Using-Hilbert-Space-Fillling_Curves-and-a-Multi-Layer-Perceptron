import matplotlib.pyplot as plot
import numpy as np
import generateGraph as getRand
# Order of the curve
ORDER = 4
# Number of quadrants required for this order HC curve
QUADRANTS = 2 ** ORDER
# Total number of vertices
TOTAL_VERTICES = QUADRANTS*QUADRANTS
# PATH
PATH = [None] * TOTAL_VERTICES
print(len(PATH))
# RESOLUTION
RESOLUTION = (100,100)

def hilbertCurve(index):
    vertices = [[0,0],[0,1],[1,1],[1,0]]
    # Getting the vertex id
    vertexId = index & 3
    # The path
    pathVector = vertices[vertexId]

    for j in range(1,ORDER):
        # Getting the quadrant to plot in
        # We right-shift each bit by two bit positions
        index = index >> 2
        # Getting the actual quadrant
        vertexId = index & 3
        # Getting the length of the edges
        edgeLength = 2**j
        # Shing the vertices to the next positions
        if vertexId == 0:
            # Using temp variable to store value of x-coordinate
            temp = pathVector[0]
            pathVector[0] = pathVector[1]
            pathVector[1] = temp
        elif vertexId == 1:
            pathVector[1] += edgeLength
        elif vertexId == 2:
            pathVector[0] += edgeLength
            pathVector[1] += edgeLength
        elif vertexId == 3:
            temp = edgeLength - 1 - pathVector[0]
            pathVector[0] = edgeLength - 1 - pathVector[1]
            pathVector[1] = temp
            pathVector[0] += edgeLength
    return pathVector


# Plotting the hilbert curve
def pathPlanner():
    height, width = RESOLUTION
    length = width/QUADRANTS
    for i in range(TOTAL_VERTICES):
        PATH[i] = hilbertCurve(i)
        PATH[i][0] *= length
        PATH[i][1] *= length
        PATH[i][0] += length/2
        PATH[i][1] += length/2

def showPath(array):
    for row in range(len(array)):
        print(array[row])
        
def drawHilbert(resolution,vertices):
    width, height = resolution
    # Initializing our axes
    x_coordinates = np.arange(0,width)
    y_coordinates = np.arange(0,height)
    figure, axes = plot.subplots(1,1)
    axes.set_xticks(x_coordinates)
    axes.set_yticks(y_coordinates)
    axes.set_xlim(0,width)
    axes.set_ylim(0,height)
    axes.grid(True)
    # Plotting
    for x,y in vertices:
        axes.plot(x,y,marker='o',markersize=1,color='red')
 

 
    plot.show()

def drawHilbertRand(resolution,vertices):
    width, height = resolution
    # Initializing our axes
    x_coordinates = np.arange(0,width)
    y_coordinates = np.arange(0,height)
    figure, axes = plot.subplots(1,1)
    axes.set_xticks(x_coordinates)
    axes.set_yticks(y_coordinates)
    axes.set_xlim(0,width)
    axes.set_ylim(0,height)
    axes.grid(True)
    # Plotting
    for setIndex in range(len(vertices)):
        currentSet = vertices[setIndex]
        x1,y1 = currentSet[0]
        x2,y2 = currentSet[1]
        axes.plot(x1,y1,marker='o',markersize=1,color='red')
        axes.plot(x2,y2,marker='o',markersize=1,color='red')

    plot.show()

pathPlanner()
nodes = getRand.getRandomPoints(PATH)
showPath(nodes)
drawHilbert(RESOLUTION,PATH)
drawHilbertRand(RESOLUTION,nodes)