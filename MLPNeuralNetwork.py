print('This is the neural network!')
import numpy as np
import sys
class NeuralNetMLP:
    """-------------------------------Parameters-------------------------------------------
        n_hidden: Number of hidden units in the hidden layer
        l2: lambda for the cross-entropy loss calculations
        epochs: number of passes of our training data
        eta: learning rate for the gradient descent
        shuffle: boolean value that shuffles the samples in our mini-batch to avoid circles
        mini_batch_size: number of training samples per minbatch
        seed: random seed for initializing our weights.

        -------------------------------Attributes-------------------------------------------
        eval_ : dictionary that collects the cost, training accuracy, and validation accuracy
        for each epoch during training.
    """
    def __init__(self, n_hidden = 30, l2 = 0, epochs = 100, eta = 0.001, shuffle = True, minibatch_size = 1, seed = None):
        self.n_hidden = n_hidden
        self.l2 = l2
        self.epochs = epochs
        self.eta = eta
        self.shuffle = shuffle
        self.minibatch_size = minibatch_size
        self.random = np.random.RandomState(seed)

    def _onehot(self, labels, unique_labels):
        """Helper function to carry out onehot encoding of our class labels. Onehot encoding
        makes it easier to train our neural networks."""
        # Creating a matrix of size samples*unique label
        onehotArray = np.zeros((unique_labels, labels.shape[0]))
        for index, value in enumerate(labels.astype(int)):
            # Adding a one to the specific (row,col) pair to indicate the specific label for a sample
            onehotArray[value-4,index]=1
        return onehotArray.T # Returning the transpose to have uniquelabels * size samples
    
    def _sigmoid(self, netInput):
        """Helper function to define the sigmoid activation functions used in our neurons."""
        return (1./(1. + np.exp(-np.clip(netInput, -250, 250))))# TODO: Change the 250s. They are specific to dataset handwritten digits
    
    def _forward(self, dataX):
        """Helper function to carry out the feed forward process."""
        # Computing net input to hidden layer
        #[n_samples, n_features] dot [n_features, n_hidden] --> [n_samples, n_hidden]
        netInput_hidden = np.dot(dataX, self.weights_hidden) + self.bias_hidden
        # Passing net input to the activation function
        activation_hidden = self._sigmoid(netInput_hidden)
        # TODO: Adding some other hidden layers
        # Adding the 2nd hidden layer
        netInput_hidden2 = np.dot(activation_hidden,self.weights_hidden2) + self.bias_hidden2
        # Passing the net input of the 2nd hidden layer to the activation units
        activation_hidden2 = self._sigmoid(netInput_hidden2)
        # Adding the 3rd hidden layer
        netInput_hidden3 = np.dot(activation_hidden2,self.weights_hidden3) + self.bias_hidden3
        # Passing the net input to the 3rd hidden layer through the activation functions
        activation_hidden3 = self._sigmoid(netInput_hidden3)
        # Calculating the net input of the output layer
        # TODO: Updating the output layer to take in values from the 2nd hidden layer
        netInput_outputLayer = np.dot(activation_hidden3, self.weights_output) + self.bias_output
        # netInput_outputLayer = np.dot(activation_hidden, self.weights_output) + self.bias_output
        # Passing the net input ot hte activation function
        activation_output = self._sigmoid(netInput_outputLayer)
                                # Result of sigmoid()
        # TODO: Update the return values.
        return netInput_hidden,activation_hidden,netInput_hidden2,activation_hidden2,netInput_hidden3,activation_hidden3,netInput_outputLayer,activation_output 
    
    def _computeCost(self,labels_enc, output):
        """Helper function to compute the cost of training our neural network.
        It uses L2 regularization."""
        # The output is an array of predicted labels from the output layer
        # [n_samples, n_output_units]

        # The cost is computed using L2 regularization-> Log loss 
        L2_term = (self.l2* (np.sum(self.weights_hidden**2.) + np.sum(self.weights_output**2.)))
        term1 = -labels_enc * (np.log(output))
        term2 = (1. - labels_enc) * np.log(1. - output)
        cost = np.sum(term1 - term2) + L2_term
        return cost
    
    def predict(self, dataX):
        """Utility function to predict the label of the points in the dataset."""
        # Carraying out the feedforward step of the neural network
        # TODO: Added variables to hold the returned values from the other 2 hidden layers
        netInput_hidden,activation_hidden,netInput_hidden2,activation_hidden2,netInput_hidden3,activation_hidden3,netInput_outputLayer,activation_output  = self._forward(dataX)
        # Picking the index of the max value/ max probability as the predicted class
        predictedLabel = np.argmax(netInput_outputLayer,axis=1)

        return predictedLabel
    
    def fit(self, trainingSet, trainingSetLabels, validationSet, validationSetLabels):
        """Utility function to train the neural network and learn the weights."""
        # Grabbing the nmber of classes
        numberOfLabels = np.unique(trainingSetLabels).shape[0]
        # Grabbing the number of features in the dataset
        numberOfFeatures = trainingSet.shape[1]
        # Initializing our weights and biases for the hidden layer
        self.bias_hidden = np.zeros(self.n_hidden)
        self.weights_hidden = self.random.normal(loc=0.0, scale=0.1,size=(numberOfFeatures, self.n_hidden))
        # Initializing the weights and biases for the 2nd hidden layer
        self.bias_hidden2 = np.zeros(self.n_hidden)
        self.weights_hidden2 = self.random.normal(loc=0.0, scale=0.1,size=(self.n_hidden, self.n_hidden))
        # Initializing the weights and biases for the 3rd hidden layer
        self.bias_hidden3 = np.zeros(self.n_hidden)
        self.weights_hidden3 = self.random.normal(loc=0.0, scale=0.1,size=(self.n_hidden, self.n_hidden))
        # Initializing our weights and biases for the output layer
        self.bias_output = np.zeros(numberOfLabels)
        self.weights_output = self.random.normal(loc=0.0, scale=0.1, size=(self.n_hidden,numberOfLabels))

        # Converting number of epochs into a string
        epochStringLength = len(str(self.epochs))
        # Hashmap to store the stats from the training process
        """Note the syntax of declaring this variable name. This is how we declare class
        properties that are initialized by class functions instead of init()"""
        self.evaluation_ = {'cost':[], 'trainingAccuracy':[], 'validationAccuracy':[]}
        # Getting the one-hot encoded labels
        trainingSetLabelOneHot = self._onehot(trainingSetLabels, numberOfLabels)

        # Iterating over each epoch
        for epoch in range(self.epochs):
            # Iterating over mini-batches
            # arange() -> returns evenly spaced values within a gien interval
            indices = np.arange(trainingSet.shape[0])

            # Shuffling our indices to keep the neural network from memorizing the dataset
            if self.shuffle:
                self.random.shuffle(indices)

            for startIndex in range(0, indices.shape[0] - self.minibatch_size + 1,self.minibatch_size):
                # Getting the current batch index
                batchIndices = indices[startIndex:startIndex+self.minibatch_size]

                ########################## FORWARD PROPAGATION ####################
                # TODO: Added variables to hold the returned values from the other 2 hidden layers
                netInputToHiddenLayer, activationHiddenLayer,netInputToHidden2, activationHidden2, netInputHidden3, activationHidden3, netInputToOutputLayer, activationOutputLayer = self._forward(trainingSet[batchIndices])
                

                ########################### BACKPROPAGATION ########################
                # Calculating the error in the predicted
                errorInOutput = activationOutputLayer - trainingSetLabelOneHot[batchIndices]
                # Getting the derivative of the sigmoid function
                # TODO: Carrying out backpropagation with extra weights and biases.
                # Calculating the derivative of activation in 3rd hidden layer
                sigmoidDerivativeHidden3 = activationHidden3 * (1. - activationHidden3)
                # Calculating the error in the 3rd hidden layer
                errorInHidden3 = (np.dot(errorInOutput,self.weights_output.T)* sigmoidDerivativeHidden3)
                # Calculating the derivative of activation in 2nd hidden layer
                sigmoidDerivativeHidden2 = activationHidden2 * (1. - activationHidden2)
                # Calculating the error in the 2nd hidden layer
                errorInHidden2 = (np.dot(errorInHidden3,self.weights_hidden3.T)*sigmoidDerivativeHidden2)
                # Calculating the derivative of the activation in 1st hidden layer
                sigmoidDerivative = activationHiddenLayer * (1. - activationHiddenLayer)
                # Calculating the error in the 1st hidden layer
                errorInHiddenLayer = (np.dot(errorInHidden2,self.weights_hidden2.T)* sigmoidDerivative)
                """
                # TODO: THE ORIGINAL BACKPROPAGATION CODE
                sigmoidDerivative = activationHiddenLayer * (1. - activationHiddenLayer)
                # Calculating the error in the hidden layer
                errorInHiddenLayer = (np.dot(errorInOutput,self.weights_output.T)* sigmoidDerivative)
                """
                # Calculating the gradients in the hidden layer
                # TODO: Calculating the gradients of new hidden layers
                # The gradients for the weights and biases of 3rd hidden layer
                gradientsOfHiddenLayer3Weights = np.dot(activationHidden2.T,errorInHidden3)
                gradientsOfHiddenLayer3Biases = np.sum(errorInHidden3, axis=0)
                # The gradients for the weights and biases of 2nd hidden layer
                gradientsOfHiddenLayer2Weights = np.dot(activationHiddenLayer.T,errorInHidden2)
                gradientsOfHiddenLayer2Biases = np.sum(errorInHidden2, axis=0)
                # The gradients for the weights and biases of 1st hidden layer
                gradientsOfHiddenLayerWeights = np.dot(trainingSet[batchIndices].T,errorInHiddenLayer)
                gradientsOfHiddenLayerBiases = np.sum(errorInHiddenLayer, axis = 0)
                # Calculating the output layer gradients
                gradientsOfOutputLayerWeights = np.dot(activationHiddenLayer.T,errorInOutput)
                gradientsOfOutputLayerBiases = np.sum(errorInOutput,axis = 0)


                ################## REGULARIZATION AND UPDATING WEIGHTS ##############
                # TODO: Updating the weights and biases of the extra hidden layers
                deltaOfHiddenLayer3Weights = (gradientsOfHiddenLayer3Weights + self.l2*self.weights_hidden3)
                deltaOfHiddenLayer3Biases = gradientsOfHiddenLayer3Biases # Bias is not regularized
                self.weights_hidden3 -= self.eta * deltaOfHiddenLayer3Weights
                self.bias_hidden3 -= self.eta * deltaOfHiddenLayer3Biases

                deltaOfHiddenLayer2Weights = (gradientsOfHiddenLayer2Weights + self.l2*self.weights_hidden2)
                deltaOfHiddenLayer2Biases = gradientsOfHiddenLayer2Biases # Bias is not regularized
                self.weights_hidden2 -= self.eta * deltaOfHiddenLayer2Weights
                self.bias_hidden2 -= self.eta * deltaOfHiddenLayer2Biases

                deltaOfHiddenLayerWeights = (gradientsOfHiddenLayerWeights + self.l2*self.weights_hidden)
                deltaOfHiddenLayerBiases = gradientsOfHiddenLayerBiases # Bias is not regularized
                self.weights_hidden -= self.eta * deltaOfHiddenLayerWeights
                self.bias_hidden -= self.eta * deltaOfHiddenLayerBiases

                deltaOfOutputLayerWeights = (gradientsOfOutputLayerWeights + self.l2*self.weights_output)
                deltaOfOutputLayerBiases = gradientsOfOutputLayerBiases # The bias is not regularized
                self.weights_output -= self.eta * deltaOfOutputLayerWeights
                self.bias_output -= self.eta * deltaOfOutputLayerBiases
            
            ##################################### EVALUATION #################################
            """Evaluation after each epoch during training is necessary. Notice that instead
            of using only a mini-batch for this forward propagation, we are using the entire
            training set. """
            # TODO: Added variables to hold the returned values from the other 2 hidden layers
            netInputToHiddenLayer, activationHiddenLayer,netInputToHidden2, activationHidden2, netInputHidden3, activationHidden3, netInputToOutputLayer, activationOutputLayer = self._forward(trainingSet)

            # Computing the cost of training the neural network
            cost = self._computeCost(labels_enc=trainingSetLabelOneHot,output=activationOutputLayer)

            # Asking our model to make predictions so that we can evaluate its performance
            trainingSetPredictedLabels = self.predict(trainingSet)
            validationSetPredictedLabels = self.predict(validationSet)
            # Returning the format from the adjusted one-hot to decimal
            trainingSetPredictedLabels += 4
            validationSetPredictedLabels += 4
            
            # Calculating the performance accuracy
            trainingSetAccuracy = ((np.sum(trainingSetLabels == trainingSetPredictedLabels)).astype(np.float64)/ trainingSet.shape[0])
            validationSetAccuracy = ((np.sum(validationSetLabels == validationSetPredictedLabels)).astype(np.float64)/validationSet.shape[0])

            sys.stderr.write('\r%0*d/%d | Cost: %.2f' '| Train/Valid Acc: %.2f%%/%.2f%%' % (epochStringLength, epoch + 1, self.epochs, cost,
                                                                                          trainingSetAccuracy*100, validationSetAccuracy*100))
            sys.stderr.flush()

            self.evaluation_['cost'].append(cost)
            self.evaluation_['trainingAccuracy'].append(trainingSetAccuracy)
            self.evaluation_['validationAccuracy'].append(validationSetAccuracy)
        return self

