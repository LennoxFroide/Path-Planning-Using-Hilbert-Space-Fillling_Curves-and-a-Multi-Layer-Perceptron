import numpy as np
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