import numpy as np
import occupancyMapGen as oMapGen
import generateFreeSpace as genFreeSpace
import loadData
import execute as executePy
def wait():
    for i in range(100):
        pass

RESOLUTION = (100,100)
length, width = RESOLUTION
"""
#-------SYNTHETIC DATA GENERATION FOR THE FIRST TIME FOR A PARTICULAR SET:TRAINING, TESTING, VALIDATION------------#
RESOLUTION = (100,100)
length, width = RESOLUTION
# To hold generated occupancy maps
occupancyMapSet = np.zeros((1,length*width))
# To hold corresponding labels
setLabels = np.zeros((1))
# The first row is just a dummy row
occupancyMapSet[0,0:10000] = None
# The first row is just a dummy row
setLabels[0] = None
# 1.) TODO: Generate a set of occupancy maps
counter = 0
while counter < 5:
    # This returns a hashMap with keys 1 -> 
    generatedMaps =  oMapGen.generateOccupancyMap(RESOLUTION)
    mapToIterate = len(generatedMaps)
    for mapIdx in range(1,mapToIterate + 1):
        # Grabbing the current occupancy map
        currentMap = generatedMaps[mapIdx]
        # Converting the map into a numpy array
        npCurrentMap = np.array(currentMap)
        # Reshaping it
        reshapedMap = np.reshape(npCurrentMap, shape=(1,length*width))
        # This append should stack the rows on top of each other
        occupancyMapSet = np.append(occupancyMapSet,reshapedMap,axis = 0)
    counter += 1
# Getting rid of the dummy row
occupancyMapSet = occupancyMapSet[1:,0:10000]
# The maps are being saved correctly
firstMap = occupancyMapSet[2]
# TODO: 2.) Automating the saving of the data
# Saving the samples-> Actual Dataset
loadData.saveNPArray(occupancyMapSet, 'trainingSet')
# Generating labels
reshapedArrays = []
reshapedMapper = {}
index = 1
for sample in occupancyMapSet:
    # Reshaping the data back to a 100*100 occupancy map
    reshapedSample = np.reshape(sample, shape=(length,width))
    # Converting reshaped array into list
    currentArray = reshapedSample.tolist()
    # Adding the occupancy map into a dinctionary
    reshapedMapper[index] = currentArray
    # Getting next key
    index += 1
# plotting the occupancy maps
oMapGen.occupanyMapPlotter(reshapedMapper)
# Generating labels
trainingLabels = executePy.execute(reshapedMapper,setLabels)
# Ssaving the labels -> Corresponding labels for the generated occupancy maps
loadData.saveNPArray(trainingLabels, 'trainingSetLabels')
wait()
"""

##-------------------------------------LOADING SAVED TRAINING SET FROM MEMORY----------------------------------------#
# TODO: 3.) Automating the loading of the data from memory
#--------------------------------------TRAINING DATASET------------------------------------------------------#
# Getting the path for the file first

filePath = loadData.getFilePath('trainingSet.npz')
# Generates a compressed file whose data can be accessed with key 'trainingSet'
loadedTrainingSetNP = loadData.loadDataNp(filePath)
# Gets the actual numpy array with all occupancy maps in it
loadedTrainingSetMaps = loadedTrainingSetNP['trainingSet']
# Gets just a single occupancy map
loadedFirstMap = loadedTrainingSetMaps[2]
#--------------------------------------TRAINING DATASET LABELS-------------------------------------------------------#
#Getting the path for the file first
filePath = loadData.getFilePath('trainingSetlabels.npz')
# Generates a compressed file whose data can be accessed with key 'trainingSet'
loadedTrainingSetNPLabels = loadData.loadDataNp(filePath)
# Gets the actual numpy array with all occupancy maps in it
loadedTrainingSetLables = loadedTrainingSetNPLabels['trainingSetLables']

##--------------------------------------TESTING WHETHER WE CAN GENERATE LABELS FOR LOADED DATA-----------------------#
"""
testingData = loadedTrainingSetMaps[1:7,0:]
reshapedArrays = []
reshapedMap = {}
index = 1
for sample in testingData:
    # Reshaping the data back to a 100*100 occupancy map
    reshapedSample = np.reshape(sample, shape=(length,width))
    # Converting reshaped array into list
    currentArray = reshapedSample.tolist()
    # Adding the occupancy map into a dinctionary
    reshapedMap[index] = currentArray
    # Getting next key
    index += 1
# plotting the occupancy maps
oMapGen.occupanyMapPlotter(reshapedMap)
# Generating labels
executePy.execute(reshapedMap)
"""
##------------------------------------ADDING MORE DATA TO A PRE-GENERATED AND SAVED COMPRESSED NUMPY ARRAY-------------#
occupancyMapSet = np.zeros((1,length*width))
# To hold corresponding labels
setLabels = np.zeros((1))
# The first row is just a dummy row
occupancyMapSet[0,0:10000] = None
# The first row is just a dummy row
setLabels[0] = None
counter = 0
while counter < 5:
    # This returns a hashMap with keys 1 -> 
    generatedMaps =  oMapGen.generateOccupancyMap(RESOLUTION)
    mapToIterate = len(generatedMaps)
    for mapIdx in range(1,mapToIterate + 1):
        # Grabbing the current occupancy map
        currentMap = generatedMaps[mapIdx]
        # Converting the map into a numpy array
        npCurrentMap = np.array(currentMap)
        # Reshaping it
        reshapedMap = np.reshape(npCurrentMap, shape=(1,length*width))
        # This append should stack the rows on top of each other
        occupancyMapSet = np.append(occupancyMapSet,reshapedMap,axis = 0)
    counter += 1
# Getting rid of the dummy row
occupancyMapSet = occupancyMapSet[1:,0:10000]
loadedTrainingSetMaps = np.append(loadedTrainingSetMaps,occupancyMapSet, axis = 0)
# Generating labels
reshapedArrays = []
reshapedMapper = {}
index = 1
for sample in occupancyMapSet:
    # Reshaping the data back to a 100*100 occupancy map
    reshapedSample = np.reshape(sample, shape=(length,width))
    # Converting reshaped array into list
    currentArray = reshapedSample.tolist()
    # Adding the occupancy map into a dinctionary
    reshapedMapper[index] = currentArray
    # Getting next key
    index += 1
# plotting the occupancy maps
oMapGen.occupanyMapPlotter(reshapedMapper)
# Generating labels
trainingLabels = executePy.execute(reshapedMapper,setLabels)
loadedTrainingSetLables = np.append(loadedTrainingSetLables,trainingLabels, axis = 0)
# Ssaving the labels -> Corresponding labels for the generated occupancy maps
# TODO: Automating the saving of the data
loadData.saveNPArray(loadedTrainingSetMaps, 'trainingSet')
loadData.saveNPArray(loadedTrainingSetLables, 'trainingSetLabels')
wait()