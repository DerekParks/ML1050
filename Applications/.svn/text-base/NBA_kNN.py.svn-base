"""
Application: NBA_kNN.py

Training Dataset: haykin2.csv
    
Description: Use kNN to classify the NBA dataset.

How to Run: python Applications/NBA_kNN.py (from root ML1050 directory)
"""
from ML1050.Preprocessing.CrossValidation import kFold
from ML1050.Classifiers.kNN import kNN
from ML1050.Example import LabeledExample
from ML1050.TrainingSet import TrainingSet

def squaredDistance(example1, example2):
    return (example1[0] - example2[0])**2 + \
           (example1[1] - example2[1])**2

def main():
    kRange = range(1, 30)
    bestValidationError, bestK = 1.0, None
    dataSet = TrainingSet('../Datasets/haykin2.csv')
    numFolds = 2
    # Find the best k
    for k in kRange:
        avgValidationError = 0
        for training, validation in kFold(dataSet, k=numFolds):
            kNNModel = kNN(k=k, distanceFunction=squaredDistance)
            kNNModel.train(training)
            error = 0.0
            for example in validation:
#                 print "example:", example
                if kNNModel.test(example) != example.label:
                    error += 1
            error = error/len(validation)
            avgValidationError += error
        avgValidationError = avgValidationError/numFolds
        print "k:", k, "average validation set error:", avgValidationError
        if avgValidationError < bestValidationError:
            bestValidationError, bestK = avgValidationError, k
    print "best k:", bestK, "average validation set error:", bestValidationError

def _test():
    """Run the tests in the documentation strings."""
    import doctest
    return doctest.testmod(verbose=False)
    
if __name__ == "__main__":
    try:
        __IP                            # Are we running IPython?
    except NameError:
        _test()                         # If not, run the tests
    main()
    
