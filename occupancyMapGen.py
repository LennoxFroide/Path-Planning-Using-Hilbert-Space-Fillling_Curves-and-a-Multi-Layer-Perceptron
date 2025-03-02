import numpy as np
import matplotlib.pyplot as plotter
import copy
import loadData

RESOLUTION = (100,100)
# difficulties = [0.1,0.35,0.8]
def generateOccupancyMap(resolution):
    difficulties = [0.989,0.996,0.998]
    # difficulties = [0.998,0.998,0.998] # Sanity check to make sure it is random enough
    hashOccupancyMaps = {}
    # Defining the dimensions of the map
    height , width = resolution
    # Adding empty spaces to the map
    occupancyMap = np.zeros((height,width), dtype=np.uint8)
    # Adding obstacles to the map
    addObstacles(occupancyMap,difficulties,hashOccupancyMaps)

    return  hashOccupancyMaps

def addObstacles(mapper,probabilities,mapperHash):
    # hashOccupancyMaps = {}
    # A map for each probability
    counter = 1
    for probability in probabilities:
        # Making a copy of the map
        # currentMap = mapper[:]
        currentMap = copy.deepcopy(mapper)
        # Grabbing the current probability
        currentProb = probability
        print(currentProb)
        # Traversing the map
        for row in range(len(currentMap)):
            for column in range(len(currentMap[row])):
                # Then we will calculate the probability of this pixel having an obstacle
                obstacleProbability = np.random.uniform(0,1,1)
                # print(obstacleProbability)
                # If this probability beats the threshold then we set the pixel to 1
                if obstacleProbability > currentProb:
                    currentMap[row][column] = 1
                else: 
                    continue
        mapperHash[counter] = currentMap
        counter += 1


generatedMaps = generateOccupancyMap(RESOLUTION)
# print(generatedMaps[2][3])
# Plotting the occupancy maps

for idx in range(1,len(generatedMaps)+1):
    plotter.imshow(generatedMaps[idx],cmap='gray')
    # Removing the ticks
    plotter.xticks([])
    plotter.yticks([])
    plotter.show()
saveReshapedData = np.empty(shape=(1,RESOLUTION[0]*RESOLUTION[1]))
loadData.saveGeneratedMaps(generatedMaps,saveReshapedData,1)