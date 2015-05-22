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
from ML1050.Utils.TrainingSetFeatureSelector import selectTrainingSetFeatures



def intToBin(i, length):
    bin = []
    num = i
    while num != 0:
        bin.append(num % 2)
        num = num/2
    while len(bin) < length:
        bin.append(0)
    return bin
    
def binToInt(myList):
    mySum = 0
    length = len(myList)
    for i in range(length):
        mySum = mySum + myList[i] * 2**i
    return mySum

            
def main():
    testSet = TrainingSet('../Datasets/SPECT.test.csv')
    k=6
    bestError=1.
    bestPattern = -1
    numOfCombinations = binToInt([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1])
    
    
    
    for i in range(1,numOfCombinations+1):
        pattern = intToBin(i, 22)
        
        #printing to check that bin conversion is sucessfull
        print "Pattern = " + str(binToInt(pattern)) + " " +str(pattern)
          
        errorSum = 0.0
        j = 0
        trainingSet = TrainingSet('../Datasets/SPECT.train.csv')
        selectTrainingSetFeatures(trainingSet, pattern)
        for training, validation in kFold(trainingSet, k):
            myNB = NaiveBayes() 
            myNB.train(training)
            errorSum = errorSum + (1-myNB.validate(validation))
            print "Fold %i complete" % (j)
            j=j+1
        avgError = errorSum / k
        if avgError < bestError:
            bestError = avgError
            bestPattern = i
        print "Avg. error = %f" % (avgError)
    
    print "Best error = " + str(bestError)
    print "best pattern = " + str(bestPattern) + " " +str(intToBin(bestPattern, 22))
    
    print "Beginning final training"
    trainingSet = TrainingSet('../Datasets/SPECT.train.csv')
    selectTrainingSetFeatures(trainingSet, intToBin(bestPattern, 22))
    myNB = NaiveBayes() 
    myNB.train(trainingSet)
    print "Finished training"
    
    
    print "Testing"
    selectTrainingSetFeatures(testSet, intToBin(bestPattern, 22))
    myNB.validate(testSet)
    myNB.confusionMatrix.display(precision = 6)

    
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

