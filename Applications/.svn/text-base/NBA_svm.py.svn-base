"""
Application: NBA_svm.py

Training Dataset: NBA_TRAIN.csv
    
Description: Use SVMs to classify the NBA dataset.

How to Run: python Applications/NBA_svm.py (from root ML1050 directory)
"""

from ML1050.External.SVM import SVM
from ML1050.Preprocessing.CrossValidation import kFold
from ML1050.Example import LabeledExample
from ML1050.TrainingSet import TrainingSet
import sys, csv, getopt, copy

def main():
    dataSet = TrainingSet('../Datasets/NBA_TRAIN.csv')
    numFolds = 10
    avgValidationError = 0
    avgTrainingError = 0
    for training, validation in kFold(dataSet, k=numFolds):
        SVMmodel = SVM()
        SVMmodel.train(dataSet)
        
        validationError = 0.0
        for example in validation:
            if SVMmodel.test(example) != example.label: validationError += 1
        validationError = float(validationError)/len(validation)
        avgValidationError += validationError
        
        trainingError = 0.0
        for example in training:
            if SVMmodel.test(example) != example.label: trainingError += 1
        trainingError = float(trainingError)/len(training)
        avgTrainingError += trainingError
    DatasetError = 0.0
    
    for example in dataSet:
        if SVMmodel.test(example) != example.label: DatasetError += 1
    DatasetError= float(DatasetError)/len(dataSet)
    
    print "\tAverage validation set error:", avgValidationError
    print "\tAverage training set error:", avgTrainingError 
    print "\tError rate when computed on whole dataset:", DatasetError, "\n" 
def _test():
    """Run all tests by docstring"""
    import doctest
    return doctest.testmod(verbose=False)

if __name__ == "__main__":
    try:
        __IP
    except NameError:
        _test()
    main()
    
