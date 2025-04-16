print('MNIST DataSet is available now!')

import os
import struct
import numpy as np
import MLPNeuralNetwork
import matplotlib.pyplot as plt
"""
PATH = ''
def loadMnistDataset(path,kind='train'):
    # Helper function to load MNIST datasets
    if kind == 'train':
        labelsPath = os.path.join(path,'%s-labels.idx1-ubyte' %kind)
        imagesPath = os.path.join(path,'%s-images.idx3-ubyte' %kind)
    else:
        labelsPath = os.path.join(path,'%s-labels.idx1-ubyte' %kind)
        imagesPath = os.path.join(path,'%s-images.idx3-ubyte' %kind)


    with open(labelsPath, 'rb') as lbPath:
        magic, n = struct.unpack('>II',lbPath.read(8))

        labels = np.fromfile(lbPath,dtype=np.uint8)

    with open(imagesPath, 'rb') as imgPath:
        magic, num, rows, cols = struct.unpack(">IIII",imgPath.read(16))
        images = np.fromfile(imgPath,dtype=np.uint8).reshape(len(labels), 784)
        images = ((images/255.) - .5) * 2

    return images, labels

trainingSet, trainingLabels = loadMnistDataset(PATH, kind='train')# For testing set we have to edit the file name template
testingSet, testingLabels =loadMnistDataset(PATH, kind='t10k')
# Saving the data into numpy compressed arrays
np.savez_compressed('mnist_scaled.npz',trainingSet = trainingSet,
                    trainingLabels = trainingLabels,
                    testingSet = testingSet,
                    testingLabels = testingLabels)
print('Rows: %d, columns: %d'%(trainingSet.shape[0],trainingSet.shape[1]))
print('Rows: %d, columns: %d'%(testingSet.shape[0],testingSet.shape[1]))
"""
# Loading the saved datasets
mnist = np.load('mnist_scaled.npz')
trainingSet = mnist['trainingSet']
trainingSetLabels = mnist['trainingLabels']
testingSet = mnist['testingSet']
testingSetLabels = mnist['testingLabels']
# Creating an instance of the neural network
neuralNet = MLPNeuralNetwork.NeuralNetMLP(n_hidden=100,l2=0.01,epochs=200,eta=0.0005,minibatch_size=100,shuffle=True,seed=1)

##################################### TRAINING THE NEURAL NETWORK #########################################3
neuralNet.fit(trainingSet=trainingSet[:55000],trainingSetLabels=trainingSetLabels[:55000],validationSet=trainingSet[55000:],validationSetLabels=trainingSetLabels[55000:])

#################################### VISUALIZING NEURAL NETWORK PERFORMANCE #############################
"""Plot showing how the training cost changes over increasing number of epochs"""
plt.plot(range(neuralNet.epochs),neuralNet.evaluation_['cost'])
plt.ylabel('Training Cost')
plt.xlabel('Number of Epochs')
plt.show()
print('MNIST DataSet is available now!')

"""Plot comparing the training accuracy versus the validatiion accuracy"""
plt.plot(range(neuralNet.epochs),neuralNet.evaluation_['trainingAccuracy'], label='training')
plt.plot(range(neuralNet.epochs),neuralNet.evaluation_['validationAccuracy'], label='validation')
plt.ylabel('Accuracy')
plt.xlabel('Number of Epochs')
plt.legend()
plt.show()

print('MNIST DataSet is available now!')

########################### APPLYING THE NEURAL NETWORK ON TESTING DATASET ############################33#
predictedTestingSetLabels = neuralNet.predict(testingSet)
testingSetPerformance = (np.sum(testingSetLabels ==predictedTestingSetLabels).astype(np.float64)/testingSet.shape[0])
print('Testing set accuracy: %.2f%%' % (testingSetPerformance*100))


