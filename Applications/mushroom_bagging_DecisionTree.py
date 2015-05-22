"""
Application: mushroom_bagging_DecisionTree.py

Training Dataset: mushroom.csv
    
Description: Application using bagging and the decision tree classifier on the
mushroom dataset.

How to Run: python Applications/mushroom_bagging_DecisionTree.py
(from root ML1050 directory)
"""

from ML1050.Classifiers.DecisionTree import DecisionTree
from ML1050.Classifiers import Bagging
from ML1050.Classifiers.Bagging import Bagging
from ML1050.Preprocessing.CrossValidation import kFold
from ML1050.Example import LabeledExample
from ML1050.TrainingSet import TrainingSet
import sys, csv, getopt, copy

def main(argv):
    testSet = []
    dataSet = TrainingSet('../Datasets/mushroom.csv')
    numFolds = 2 
    theta = 0.19
    data = []
    avgValidationError = 0
    avgTrainingError = 0
    for training, validation in kFold(dataSet, k=numFolds):
        DTmodel = DecisionTree(theta)
        bagger = Bagging(copy.deepcopy(DTmodel), 20)
        bagger.train(dataSet)
        validationError = 0.0
        for example in validation:       
            if bagger.test(example) != \
            example.label: validationError += 1
        #compute validation error
        validationError = float(validationError)/len(validation)
        avgValidationError += validationError
        trainingError = 0.0
        for example in training:
            if bagger.test(example) != example.label: trainingError += 1
        #compute training error
        trainingError = float(trainingError)/len(training)
        avgTrainingError += trainingError
    DatasetError = 0    
    for example in dataSet:
        if bagger.test(example) != example.label: DatasetError += 1
    #compute error on the eitire dataset
    DatasetError= float(DatasetError)/len(dataSet)
    avgValidationError = avgValidationError/numFolds
    avgTrainingError = avgTrainingError/numFolds
    #compute test set if provided with a testset
    testError = 0.0
    if len(testSet) > 0:
        for example in testSet:
            if bagger.test(example) != example.label: testError += 1
        testError = float(testError)/len(testSet)
    #print error rates
    print "Theta:", theta, \
    "\n\tAverage validation set error:", avgValidationError
    print "\tAverage training set error:", avgTrainingError 
    print "\tError rate when computed on whole dataset:", DatasetError, \
    "\n"
    if len(testSet) > 0: print "\tTest Set Error:", testErrori

def _test():
    """Run the tests in the documentation string."""
    import doctest
    return doctest.testmod(verbose=False)

if __name__ == "__main__":
    try:
            __IP                            # Are we running IPython?
    except NameError:
        _test()                         # If not, run the tests
    main(sys.argv[1:])


