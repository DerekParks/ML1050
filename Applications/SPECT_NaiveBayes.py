"""
Application: SPECT_NaiveBayes.py

Training Dataset: SPECT.csv
    
Description: Use NaiveBayes to classify the SPECT dataset.

How to Run: python SPECT_NaiveBayes.py (from inside ML1050/Applications)
"""

from ML1050.Classifiers.NaiveBayes import NaiveBayes
from ML1050.TrainingSet import TrainingSet
from ML1050.Example import LabeledExample
from ML1050.Preprocessing.CrossValidation import kFold
import cPickle
from ML1050.Utils.ConfusionMatrix import ConfusionMatrix
            
def main():
    trainingSet = TrainingSet('../Datasets/SPECT.train.csv')
    testSet = TrainingSet('../Datasets/SPECT.test.csv')
    fileName = "SPECT_NaiveBayes.pickle"
    k=6
    bestError=1.
    
    errorSum = 0.0
    j = 0
    for training, validation in kFold(trainingSet, k):
        myNB = NaiveBayes() 
        myNB.train(training)
        errorSum = errorSum + (1-myNB.validate(validation))
        print "Fold %i complete" % (j)
        j=j+1
    avgError = errorSum / k
    if avgError < bestError:
        bestError = avgError
    print "Avg. error = %f" % (avgError)
    
    print "Beginning final training"
    myNB = NaiveBayes() 
    myNB.train(trainingSet)
    print "Finished training"
    
    print "Testing"
    myNB.validate(testSet)
    myNB.confusionMatrix.display(precision = 6)
    
    myNB.serialize(fileName)
    print "Naive Bayes sucessfully pickled"
    print "Output file is \"" + fileName + "\""
    
def _test():
    import doctest
    return doctest.testmod(verbose=False)

if __name__ == "__main__":
    try:
        __IP                            # Are we running IPython?
    except NameError:
        _test()                         # If not, run the tests
        #main(sys.argv[1:])
    main()

