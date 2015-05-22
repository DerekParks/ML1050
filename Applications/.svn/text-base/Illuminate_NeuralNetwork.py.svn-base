"""
Application: mushroom_NeuralNetwork.py

Training Dataset: mushroom.csv
    
Description: Use NeuralNetwork to classify the mushroom dataset.
See GenericNeuralNetworkApp for usage
"""

import sys
from ML1050.Utils.GenericNeuralNetworkApp import GenericNeuralNetworkApp   

if __name__ == "__main__":
    try:
        __IP                            # Are we running IPython?
    except NameError:
   
        GenericNeuralNetworkApp(sys.argv[1:], 
             './Illuminate_NeuralNetwork.pickle', 
             '../Datasets/Illuminate.csv',
             range(1,101, 10),
             [0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
             [10, 30, 50, 100, 150, 200, 300], {'doInputs':False}, False, searchEpocs=100)
