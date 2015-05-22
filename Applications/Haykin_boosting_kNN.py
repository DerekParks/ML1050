"""
Application: Haykin_boosting_kNN.py

Training Dataset: haykin2.csv
    
Description: Boosting for the Haykin dataset using AdaBoost

How to Run: python Applications/latLong_DecisionTree.py
(from root ML1050 directory)
"""

from ML1050.Preprocessing.CrossValidation import kFold
from ML1050.Classifiers.kNN import kNN
from ML1050.Example import LabeledExample
from ML1050.TrainingSet import TrainingSet
from ML1050.Classifiers.AdaBoost import AdaBoost
import copy

def main():
    """Application body"""
    trainingSet = TrainingSet('../Datasets/haykin2.csv')
    validK = range(1, 30)
    optimalK = 1.0
    bestK = None
    numFolds = 2
    
    for index in validK:
        avgValidationError = 0
        for training, validation in kFold(trainingSet, k = numFolds):
            kNNModel = kNN(index, attributeDistance)
            AdaModel = AdaBoost()
            AdaModel.train(copy.deepcopy(kNNModel),trainingSet,M=100)
            error = 0.0
            for example in validation:
                if Adamodel.text(example) != example.label:
                    error += 1
            error = error/len(validation)
            avgValidationError += error
        avgValidationError = avgValidationError/numFolds
        print "k:", index, "with average validation set error:", avgValidationError
        if avgValidationError < optimalK:
            optimalK, bestK = avgValidationError, index
    print "Best k:", bestK, "with average validation set error:", bestValidationError
    
def _test():
    import doctest
    return doctest.testmod(verbose=False)

def attributeDistance(example1, example2):
    nequals = lambda f,s: f != s
    result = map(nequals,example1, example2)
    return sum(result)

if __name__ == "__main__":
    try:
        __IP
    except NameError:
        _test()
        main()