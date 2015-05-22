"""
Application: mushroom_NeuralNetwork.py

Training Dataset: mushroom.csv
    
Description: Use NeuralNetwork to classify the mushroom dataset.

How to Run: python mushroom_NeuralNetwork.py [testSet] (from inside ML1050/Applications)
"""

from ML1050.Classifiers.TanhNeuralNetwork import TanhNeuralNetwork
from ML1050.TrainingSet import TrainingSet
from ML1050.Example import LabeledExample
from ML1050.Preprocessing.NNPreprocessing import NNPreprocessing
from ML1050.Preprocessing.CrossValidation import kFold
import cPickle
            
def main():
    trainingSet = TrainingSet('../Datasets/mushroom.csv')
    preproc = NNPreprocessing(trainingSet, expandTwo = True)
    
    bestHiddenUnits = 0
    k=10
    epochs=50
    bestError=1.
    
    
    for i in range(1,7):
        print "Training with %i hidden units" % (i)
        j = 1
        errorSum = 0.
        for training, validation in kFold(trainingSet, k):
            myNN = TanhNeuralNetwork(inputs = len(training[0]), 
                             outputs = len(training[0].label), 
                             regression = False,
                             hiddenUnits = i,
                             learningRate=0.3)
            myNN.train(training, epochs, 0)
            errorSum = errorSum + myNN.validate(validation)[0]
            print "Fold %i complete" % (j)
            j=j+1
        avgError = errorSum / k
        if avgError < bestError:
            bestError = avgError
            bestHiddenUnits = i
        print "Avg. error for %i hidden units = %f" % (i,avgError)

    
    print "Best number of hidden units = %i" % (bestHiddenUnits)
    print "Best error = %f" % (bestError)
    print "Beginning final training"
    myNN = TanhNeuralNetwork(inputs = len(trainingSet[0]), 
                     outputs = len(trainingSet[0].label), 
                     regression = False,
                     hiddenUnits = i,
                     learningRate=0.3)
    myNN.train(trainingSet, epochs, 0)
    print "Finished training"
    outFile = open('mushroom_TanhNeuralNetwork_pickle.txt' , 'wb')
    cPickle.dump(myNN, outFile)
    outFile.close()
    print "Neural network sucessfully pickled"
    print "Output file is \"mushroom_TanhNeuralNetwork_pickle.txt\""
    

    
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

