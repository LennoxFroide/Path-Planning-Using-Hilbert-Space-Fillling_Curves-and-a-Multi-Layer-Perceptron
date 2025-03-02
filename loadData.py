import numpy as np
import os

directoryPath = os.getcwd()
trainingPath = 'dataset.npz'
trainingDataPath = os.path.join(directoryPath,trainingPath)
RESOLUTION = (100,100)

# Saving our generated occupancy maps
def saveGeneratedMaps(occupancyHashMap,totalDataSet,saveCounter):
    #TODO: We need to store the counter as well
    length, width = RESOLUTION
    """This helper function used the numpy compressed savez function
    to save our occupancy maps."""
    # We first have to reshape each occupancy map into a vector 
    for index in range(saveCounter, saveCounter + len(occupancyHashMap)):
        # Grabbing one map
        currentMap = occupancyHashMap[index]
        # Calling reshape method on it
        reshapedMap = np.reshape(currentMap, shape=length*width)
        np.append(totalDataSet,reshapedMap)
    np.savez_compressed('dataset.npz',trainingSet = totalDataSet)

def loadDataNp(path):
    maps = np.load(path,allow_pickle=True)
    return maps

trainingSet = loadDataNp(trainingDataPath)
print(np.shape(trainingSet['trainingSet']))
# print(t)
# print(trainingSet.shape[0])