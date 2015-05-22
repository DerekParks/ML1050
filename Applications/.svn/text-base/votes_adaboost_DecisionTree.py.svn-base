"""
Application: votes_AdaBoost_DecisionTree.py

Training Dataset: votes-train0.csv
    
Description: This application will compare an X node decision tree versus Y one-node 
decision trees using AdaBoost. It uses the voting record dataset which will classify
democrats and republicans. Will get different validation and training errors each run
because uses kfold and builds a new tree each run. Hardcoded the best theta, which 
was found during cross validation.

How to Run: python Applications/votes_DecisionTree.py (from root ML1050 directory)
"""

from ML1050.Classifiers.DecisionTree import DecisionTree
from ML1050.Classifiers.AdaBoost import AdaBoost
from ML1050.Preprocessing.CrossValidation import kFold
from ML1050.Example import LabeledExample
from ML1050.TrainingSet import TrainingSet
import sys, csv, getopt, copy

def main():
    #Initialize the test set, not needed since we aren't going to
    # specify a test set.
    testSet = []
    
    #Load in the dataset for training
    dataSet = TrainingSet('../Datasets/votes-train0.csv')
    #DTmodel.train(dataSet)
    
    #Set the number of folds
    numFolds = 10
    
    #Set the theta value. (Said to be the best)
    theta = 0.2325
    
    #(Not currently used) For writing results to a file.
    data=[]

    #Here, we set up the AdaBoost validation error the same way as the
    # decison tree validation Error.
    avgValidationError = 0
    avgAdaValidationError = 0
    
    #We do the same for training error.
    avgTrainingError = 0
    avgAdaTrainingError = 0
    
    #First, we build the X node Decision Tree and our AdaBoost model.
    # Second, we train both models on the dataset.
    # Last, we test the models and see how they do.
    for training, validation in kFold(dataSet, k=numFolds):
        #Build the Decision Tree
        DTmodel = DecisionTree(theta,maxDepth=10)
        
        #Create a one node Decision Tree for AdaBoost to use
        DTAdamodel = DecisionTree(theta,maxDepth=1)
        
        #Train the Decision Tree
        DTmodel.train(dataSet)
        
        #Set up AdaBoost
        AdaModel = AdaBoost(DTAdamodel,M=100)
        AdaModel.train(dataSet,useSamples=True)
        
        #initialize error, used later to calculate average error
        validationError = 0.0
        adaValidationError = 0.0
        for example in validation:
            #try to test the model...
            #will return AttributeError when the entropy of the 
            #origional dataSet was <= the current value of theta
            #Because no tree was ever generated.  
            try:
                if DTmodel.test(example) != example.label: validationError += 1
                if AdaModel.test(example) != example.label: adaValidationError += 1
            except AttributeError: 
                #If you got here, you forgot to train the model.
                print "AttributeError"
                return
        #compute validation error
        validationError = float(validationError)/len(validation)
        adaValidationError = float(adaValidationError)/len(validation)
        avgAdaValidationError += adaValidationError
        avgValidationError += validationError
        
        #Begin testing training error
        trainingError = 0.0
        adaTrainingError = 0.0
        for example in training:
            if DTmodel.test(example) != example.label: trainingError += 1
            if AdaModel.test(example) != example.label: adaTrainingError += 1
        #compute training error
        trainingError = float(trainingError)/len(training)
        adaTrainingError = float(adaTrainingError)/len(training)
        avgTrainingError += trainingError
        avgAdaTrainingError += adaTrainingError
    #End Training and validation loop
    
    #Begin overall dataset error. This is testing includes the entire dataset.
    DatasetError = 0
    adaDatasetError = 0
    for example in dataSet:
        if DTmodel.test(example) != example.label: DatasetError += 1
        if AdaModel.test(example) != example.label: adaDatasetError += 1
    #compute error on the entire dataset
    DatasetError= float(DatasetError)/len(dataSet)
    adaDatasetError= float(adaDatasetError)/len(dataSet)
    
    #Compute averages
    avgValidationError = avgValidationError/numFolds
    avgAdaValidationError = avgAdaValidationError/numFolds
    avgTrainingError = avgTrainingError/numFolds
    avgAdaTrainingError = avgAdaTrainingError/numFolds
    
    #Compute test set error if user provided a testset (Not currently used)
    testError = 0.0
    adaTestError = 0.0
    if len(testSet) > 0:
        for example in testSet:
            if DTmodel.test(example) != example.label: testError += 1
            if AdaModel.test(example) != example.label: adaTestError += 1
        testError = float(testError)/len(testSet)
        adaTestError = float(adaTestError)/let(testSet)
    
    #print error rates
    print "Theta:", theta
    print "\tAverage validation set error:", avgValidationError
    print "\tAverage training set error:", avgTrainingError 
    print "\tError rate when computed on whole dataset:", DatasetError, \
    "\n" 
    if len(testSet) > 0:
        print "\tTest Set Error:", testError
    print "\n\nUsing AdaBoost"
    print "\tAverage validation set error:", avgAdaValidationError
    print "\tAverage training set error:", avgAdaTrainingError 
    print "\tError rate when computed on whole dataset:", adaDatasetError, \
    "\n" 
    if len(testSet) > 0:
        print "\tTest Set Error:", adaTestError
        
    #There was old code here that would write output to a file.
    # it's gone now, but it will be remembered as long as this
    # comment is still here. It was only useful when searching
    # for the optimal theta.
    
#Given that we don't write results to a file, this isn't much use.
# You know, as far as functions go. But, it remains in case we want
# to change that.
def PrintResults(bestTheta, bestValidationError, data):
    print "Best Theta:", bestTheta, \
    "\nAverage validation set error:", bestValidationError        
    #print data
    filename = "votesOut.log"
    writeFile(filename, data)    

#writeFile is linked to PrintResults, it gets to stay too.
def writeFile(fileName, data):
        logfile = csv.writer(file(fileName, 'w'))
        for entry in data:
                logfile.writerow(entry)
        #logfile.close()

#Run the tests in the documentation string. (Of which there are
# none).
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


