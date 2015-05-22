"""
Application: mushroom_DecisionTree.py

Training Dataset: mushroom.csv
    
Description: Use a Decision Tree to classify the mushroom dataset. Will get different
validation and training errors each run because uses kfold and builds a new tree each
run. Hardcoded the best theta, which was found during cross validation.

How to Run: python Applications/mushroom_DecisionTree.py (from root ML1050 directory)

TODO: 1. Comment better
"""

from ML1050.Classifiers.DecisionTree import DecisionTree
from ML1050.Preprocessing.CrossValidation import kFold
from ML1050.Example import LabeledExample
from ML1050.TrainingSet import TrainingSet
import sys, csv, getopt

def main(argv):
    #make the max theta sys.maxint so can use this with other datasets that have 
    #more than 2 classes (max entropy varies depending on # classes)
    #allow the user to supply a testset with the t switch
    try:
        opts, args = getopt.getopt(argv, "t:", ["testset="])
    except getopt.GetoptError:
        sys.exit(2)
    testFile = "none"
    for opt, arg in opts:
        if opt in ("-t", "--testset"): testFile = arg
    if testFile != "none": testSet = TrainingSet(testFile)
    else: testSet = []

    #thetaMax = sys.maxint 
    #bestValidationError, bestTheta = 1.0, None
    dataSet = TrainingSet('Datasets/mushroom.csv')
    numFolds = 2 
    theta = 0.19
    #increment = 0.0025
    #data=[]
    #Find the best value for theta
    #while theta < thetaMax:
    '''took out this loop...was used for finding theta'''
    avgValidationError = 0
    avgTrainingError = 0
    for training, validation in kFold(dataSet, k=numFolds):
        DTmodel = DecisionTree(theta)
        DTmodel.train(dataSet)
        validationError = 0.0
        for example in validation:
            #try to test the model...
            #will return AttributeError when the entropy of the 
            #origional dataSet was <= the current value of theta
            #Because no tree was ever generated.  
            try:
                if DTmodel.test(example) != \
                example.label: validationError += 1
            except AttributeError: return
        #compute validation error
        validationError = float(validationError)/len(validation)
        avgValidationError += validationError
        trainingError = 0.0
        for example in training:
            if DTmodel.test(example) != example.label: trainingError += 1
        #compute training error
        trainingError = float(trainingError)/len(training)
        avgTrainingError += trainingError
    DatasetError = 0    
    for example in dataSet:
        if DTmodel.test(example) != example.label: DatasetError += 1
    #compute error on the eitire dataset
    DatasetError= float(DatasetError)/len(dataSet)
    avgValidationError = avgValidationError/numFolds
    avgTrainingError = avgTrainingError/numFolds
        #compute test set if provided with a testset
    testError = 0.0
    if len(testSet) > 0:
        for example in testSet:
            if DTmodel.test(example) != example.label: testError += 1
        testError = float(testError)/len(testSet)
    #print error rates
    print "Theta:", theta, \
    "\n\tAverage validation set error:", avgValidationError
    print "\tAverage training set error:", avgTrainingError 
    print "\tError rate when computed on whole dataset:", DatasetError, \
    "\n"
    if len(testSet) > 0: print "\tTest Set Error:", testErrori
    
'''this was used to find the best value for theta durint corss validation'''
    #if avgValidationError < bestValidationError:
    #    bestValidationError, bestTheta = avgValidationError, theta
    #data.append([theta, avgValidationError, avgTrainingError, DatasetError])
    #theta += increment
'''end of loop I took out'''
    #print info to file for graphing purposes 
    #PrintResults(bestTheta, bestValidationError, data)
            
def PrintResults(bestTheta, bestValidationError, data):
    '''prints training/validaiton error to a file for graphing purposes'''
    print "Best Theta:", bestTheta, \
    "\nAverage validation set error:", bestValidationError        
    #print data
    filename = "mushroomOut.log"
    writeFile(filename, data)    

def writeFile(fileName, data):
        logfile = csv.writer(file(fileName, 'w'))
        for entry in data: logfile.writerow(entry)
        #logfile.close()

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


