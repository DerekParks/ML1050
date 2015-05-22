"""
Application: SPECT_TanhNeuralNetwork.py

Training Dataset: SPECT.csv
    
Description: Use NeuralNetwork to classify the SPECT dataset.

How to Run: python SPECT_NeuralNetwork.py(from inside ML1050/Applications)
"""

from ML1050.Classifiers.TanhNeuralNetwork import TanhNeuralNetwork
from ML1050.TrainingSet import TrainingSet
from ML1050.Example import LabeledExample
from ML1050.Preprocessing.NNPreprocessing import NNPreprocessing
from ML1050.Preprocessing.CrossValidation import kFold
import cPickle
from ML1050.Utils.ConfusionMatrix import ConfusionMatrix
import random
            
def main():
    trainingSet1 = TrainingSet('../Datasets/SPECT.train.csv')
    
    #create new trainingSet with appropriate balance
    for e in trainingSet1[::-1]:
        if e.label == '0':
            trainingSet1.remove(e)
    trainingSet = TrainingSet('../Datasets/SPECT.train.csv')
    for i in range(458):
        index = random.randint(0,len(trainingSet1)-1)
        ex = LabeledExample(trainingSet1[index][:], label = trainingSet1[index].label)
        trainingSet.append(ex)
    random.shuffle(trainingSet)

    testSet = TrainingSet('../Datasets/SPECT.test.csv')
    preproc = NNPreprocessing(trainingSet, expandTwo = True, forceStr=True, doInputs=False)
    fileName = "SPECT_TanhNeuralNetwork_pickle.pickle"
    bestHiddenUnits = 0
    k=4
    epochs=400
    bestError=1.
    threshold = 0.01
    
    
    for i in range(5,16):
        print "Training with %i hidden units" % (i)
        j = 1
        errorSum = 0.
        for training, validation in kFold(trainingSet, k):
            myNN = TanhNeuralNetwork(NNPreproc = preproc, 
                             inputs = len(training[0]), 
                             outputs = len(training[0].label),
                             hiddenUnits = i,
                             learningRate=0.2,
                             momentumRate = 0.8, \
                             adaptiveLearning = True, \
                             adaptiveHistory = 10, \
                             adaptiveAlpha = 0.05, \
                             adaptiveBeta = 2.0)
            myNN.train(training, epochs, threshold)
            errorSum = errorSum + myNN.validate(validation, translate = False)
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
    myNN = TanhNeuralNetwork(NNPreproc = preproc, 
                     inputs = len(trainingSet[0]), 
                     outputs = len(trainingSet[0].label),
                     hiddenUnits = bestHiddenUnits,
                     learningRate=0.2,
                     momentumRate = 0.8, \
                     adaptiveLearning = True, \
                     adaptiveHistory = 10, \
                     adaptiveAlpha = 0.05, \
                     adaptiveBeta = 2.0)
    myNN.train(trainingSet, epochs, threshold)
    print "Finished training"
    
    print "Testing"
    cm = myNN.test(testSet)
    cm.display(precision = 6)
    
    myNN.serialize(fileName)
    print "Neural network sucessfully pickled"
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

