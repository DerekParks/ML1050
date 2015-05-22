"""
Application: SPECT_DecisionTree.py

Training Dataset: SPECT.csv
    
Description: Use DecisionTree to classify the SPECT dataset.

How to Run: python SPECT_DecisionTree.py (from inside ML1050/Applications)
"""

from ML1050.Classifiers.DecisionTree import DecisionTree
from ML1050.TrainingSet import TrainingSet
from ML1050.Example import LabeledExample
from ML1050.Preprocessing.CrossValidation import kFold
import cPickle
from ML1050.Utils.ConfusionMatrix import ConfusionMatrix
            
def main():
    trainingSet = TrainingSet('../Datasets/SPECT.train.csv')
    testSet = TrainingSet('../Datasets/SPECT.test.csv')
    fileName = "SPECT_DecisionTree.pickle"
    k=6
    bestError=1.
    increment = 0.01
    
    for i in range(1,99):
        theta = increment*i
        print "Training with theta %f" % (theta)
        j = 1
        errorSum = 0.
        for training, validation in kFold(trainingSet, k):
            validationError = 0.0
            myDT = DecisionTree(theta) 
            myDT.train(training)
            for example in validation:
                if myDT.test(example) != example.label:
                    validationError += 1
            errorSum = errorSum + float(validationError)/len(validation)
            print "Fold %i complete with error %f" % (j,float(validationError)/len(validation))
            j=j+1
        avgError = errorSum / k
        if avgError < bestError:
            bestError = avgError
            bestTheta = theta
        print "Avg. error for theta %f = %f" % (theta,avgError)
    
    print "Best theta = %f" % (bestTheta)
    print "Best error = %f" % (bestError)
    print "Beginning final training"
    myDT = DecisionTree(bestTheta) 
    myDT.train(trainingSet)
    print "Finished training"
    
    print "Testing"
    cm = ConfusionMatrix([],[])
    for example in testSet:
        cm.addRecord(myDT.test(example), example.label)
    cm.build()
    cm.display(precision = 6)
    
    # It looks like Decision Tree cannot be serialized yet
    #myDT.serialize(fileName)
    #print "DecisionTree sucessfully pickled"
    #print "Output file is \"" + fileName + "\""
    


    
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

