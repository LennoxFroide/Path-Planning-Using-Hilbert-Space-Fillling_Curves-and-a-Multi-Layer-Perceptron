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
            onehotArray[value, index] = 1
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
        # Calculating the net input of the output layer
        netInput_outputLayer = np.dot(activation_hidden, self.weights_output) + self.bias_output
        # Passing the net input ot hte activation function
        activation_output = self._sigmoid(netInput_outputLayer)
                                # Result of sigmoid()
        return netInput_hidden,   activation_hidden,    netInput_outputLayer,     activation_output 
    
    
    pass