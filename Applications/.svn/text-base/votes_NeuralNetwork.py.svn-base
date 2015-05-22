"""
Application: votes_NeuralNetwork.py

Training Dataset: votes-train0.csv
    
Description: Use NeuralNetwork to classify the votes dataset.
See GenericNeuralNetworkApp for usage
"""

import sys
from ML1050.Utils.GenericNeuralNetworkApp import GenericNeuralNetworkApp 


if __name__ == "__main__":
    try:
        __IP                            # Are we running IPython?
    except NameError:
   
        GenericNeuralNetworkApp(sys.argv[1:], 
             './votes_NeuralNetwork.pickle', 
             '../Datasets/votes-train0.csv',
             [1,2,3,4,5,6,7,8,9,10],
             [0.025,0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6,0.7,0.8],
             [10, 30, 50, 100, 150, 200, 300, 500])

