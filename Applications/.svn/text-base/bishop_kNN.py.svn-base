"""
Application: bishop_kNN.py

Training Dataset: bishop_synthetic.csv
    
Description: kNN classifier to classify Bishop's synthetic dataset.

How to Run: python Applications/bishop_kNN.py
(from root ML1050 directory)
"""

from ML1050.Preprocessing.CrossValidation import kFold
from ML1050.Classifiers.kNN import kNN
from ML1050.Example import LabeledExample
from ML1050.TrainingSet import TrainingSet

# the distance function to used for kNN.
def distanceFunction(ex1, ex2):
   dist = len(ex1)
   for i in range(len(ex1)):
      if ex1[i] == ex2[i]:
         dist -= 1
   return dist

def main():
    # the training set to be used for this application
    trainingSet = TrainingSet('../Datasets/bishop_synthetic.csv')   
    kRange = range(1, 30)
    bestValidationError, bestK = 1.0, None
    numFolds = 2
    #find the best k within the given range.  This takes a very long time when
    #using bagging
    for j in kRange:
       avgValidationError = 0
       for training, validation in kFold(trainingSet, k = numFolds):
          kNNModel = kNN(j, distanceFunction)
          kNNModel.train(training)
          error = 0.0
          for example in validation:
             if kNNModel.test(example) != example.label:
                error+=1
          error = error/len(validation)
          avgValidationError += error
       avgValidationError = avgValidationError/numFolds
       print "k:", j, "average validation set error:", avgValidationError
       if avgValidationError < bestValidationError:
          bestValidationError, bestK = avgValidationError, j
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

