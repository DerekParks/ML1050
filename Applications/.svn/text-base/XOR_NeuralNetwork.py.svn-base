"""
Application: XOR_NeuralNetwork.py

Training Dataset: XOR.csv
    
Description: Use NeuralNetwork to classify the XOR dataset.

How to Run: python Applications/XOR_NeuralNetwork.py (from root ML1050 directory)
"""

from ML1050.Classifiers.NeuralNetwork import  NeuralNetwork
from ML1050.TrainingSet import TrainingSet
from ML1050.Example import LabeledExample
from ML1050.Preprocessing.NNPreprocessing import NNPreprocessing

def main():

    myNN = NeuralNetwork(inputs = 2, outputs = 1, hiddenUnits = 2,learningRate=0.3)

    trainingSet = TrainingSet('../Datasets/XOR.csv')
    
    preproc = NNPreprocessing(trainingSet)
    
    myNN.train(trainingSet,200000, 0.0001)

    print "Network Weights"
    print myNN
    
    for ex in trainingSet:
        print "Ex:", ex, "Got:", myNN(ex)

    print "Total Error:",myNN.validate(trainingSet)
    

if __name__ == "__main__":
    try:
        __IP                            # Are we running IPython?
    except NameError:
        main()
