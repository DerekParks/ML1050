"""

"""
from ML1050.Preprocessing.CrossValidation import kFold
from ML1050.Classifiers.simplekNN import kNN
from ML1050.Example import LabeledExample
from ML1050.TrainingSet import TrainingSet

def squaredDistance(l1, l2):
    return sum([ (l1[i] - l2[i])**2 for i in range(len(l1)) ])


def getFN(validation, knn):
    numFN =0.
    numN = 0.
    for example in validation:
        if example.label == '0':
            print example.label, knn.test(example), knn.test(example)#, knn.test(example) == '1'
            numN += 1
            if knn.test(example) == '1':
                print "\t",example.label, knn.test(example)
                numFN += 1
    return numFN/numN

def main():
    kRange = range(1, 10)
    bestValidationError, bestK = 1.0, None
    #dataSet = TrainingSet('../Datasets/Illuminate.csv')
    dataSet = TrainingSet('../Datasets/Illuminate25x25.csv')
    numFolds = 4
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
    
    kNNModel = kNN(k=k, distanceFunction=squaredDistance)
    kNNModel.train(dataSet)
    
    print "Training Error on entire data set", kNNModel.validate(dataSet)
    print "FN rate: ", getFN(dataSet, kNNModel)



def _test():
    """Run the tests in the documentation strings."""
    import doctest
    return doctest.testmod(verbose=False)
    
if __name__ == "__main__":
    try:
        __IP                            # Are we running IPython?
    except NameError:
        #_test()                         # If not, run the tests
        main()
    
