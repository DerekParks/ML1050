"""
How to Run: python %s [options]

Options:
    -h    --help          Print this message
    -d    --debug         Print debug messages
    -l    --graphHL       Show graph of error for all hidden units and learning rates
    -e    --graphEpocs    Show graph of error vs number of epocs of training
    -t    --testSet=file  Test with given test set
    --forceHLCalc         Force recalculation of error for all hidden units and learning rates
    --forceEpocCalc       Force recalculation of error vs number of epocs of training
    --forceNNBuild        Force creation and training of NN 
    --trainingError       Print the training error from the entire training set
"""

from ML1050.Classifiers.NeuralNetwork import NeuralNetwork
from ML1050.TrainingSet import TrainingSet
from ML1050.Example import LabeledExample
from ML1050.Preprocessing.NNPreprocessing import NNPreprocessing
from ML1050.Preprocessing.CrossValidation import kFold
from ML1050.Utils.NNParameterSearch import NNParameterSearch
from Numeric import arange
import sys,os, cPickle, getopt, logging

def GenericNeuralNetworkApp(argv, 
         saveFilePath, 
         trainingSetPath, 
         rangeHiddenUnits, 
         rangeLearningRate,
         rangeEpocs,
         preprocessingArgs = {}, regression=True, searchEpocs=30):

    
    try:                                
        opts, args = getopt.getopt(sys.argv[1:], 
                                   "hdlest:", 
                                   ["help",
                                    "debug",
                                    "graphHL", 
                                    "graphEpocs", 
                                    "testSet=", 
                                    "forceHLCalc",
                                    "forceEpocCalc",
                                    "forceNNBuild",
                                    "trainingError",
                                    "forceSearch"])
 
    except getopt.GetoptError:
        print __doc__ % (sys.argv[0])
        sys.exit(2)
    
    if len(opts) == 0:
        print __doc__ % (sys.argv[0])
        sys.exit(2)
    
    showHLGraph = False
    showEpocGraph = False
    testSetPath = None
    forceHL = False
    forceEpoc = False
    forceNN = False
    trainingError = False
    forceSearch = False
    
    logLevel = logging.NOTSET
    for opt, arg in opts:           
        if opt in ("-h", "--help"):      
            print __doc__ % (sys.argv[0])               
            sys.exit()                  
        elif opt in ("-d", "--debug"):    
             logLevel = logging.DEBUG
        elif opt in ("-l", "--graphHL"):    
             showHLGraph = True
        elif opt in ("-e", "--graphEpocs"):    
             showEpocGraph = True    
        elif opt in ("-t", "--testSet"):    
             testSetPath = arg
        elif opt in ("--forceHLCalc"):    
             forceHL = True
        elif opt in ("--forceEpocCalc"):    
             forceEpoc = True        
        elif opt in ("--forceNNBuild"):    
             forceNN = True  
        elif opt in ("--trainingError"):
             trainingError = True
        elif opt in ("-s", "--forceSearch"):
             forceSearch = True
    logging.basicConfig(level=logLevel)
    logging.debug("Training Set Path: %s" % (trainingSetPath))
    
    trainingSet = TrainingSet(trainingSetPath)

    preproc = NNPreprocessing(trainingSet, **preprocessingArgs)
    
    dumpNetwork = False
    if os.path.exists(saveFilePath) and not forceSearch:
        
        thisNN = cPickle.load(open(saveFilePath,'r'))
        logging.debug("Found NN on disk. No need to calculate parameters.")
    
    else:
        logging.debug("NN NOT found on disk. Parameters will be calculated. This will take some time.")
        search = NNParameterSearch(inputs=len(trainingSet[0]),
                                   outputs=len(trainingSet[0].label),
                                   logLevel=logLevel, regression=regression)
        
        search.calcHL(trainingSet, rangeHiddenUnits, rangeLearningRate, searchEpocs)

        h, l = search.getHiddenUnitsAndLearningRate()
        search.calcEpocs(trainingSet, rangeEpocs, h, l)
        
        thisNN = search.getBestNN(trainingSet, 0.0001)
        thisNN.search = search
        
        dumpNetwork = True


    if showHLGraph:
        thisNN.search.graphHL(['r-', 'b-', 'y-', 'm-', 'c-', 'w-', 'g-', 'k-', 'r--','b--', 'y--', 'm--', 'c--', 'w--', 'g--', 'k--'])

    if showEpocGraph:
        thisNN.search.graphEpocs()   

    if testSetPath is not None:
        logging.debug("Validating with Test set: %s"% (testSetPath))
        testSet = TrainingSet(testSetPath)
        preprocTest = preproc.forward(testSet)
        
        print "Test Error:", thisNN.validate(testSet)[0]

    if forceHL:
        logging.debug("Recalculating best number of hidden units and learning rate")
        thisNN.search.calcHL(trainingSet, rangeHiddenUnits, rangeLearningRate, 30)
        dumpNetwork = True
    
    if forceEpoc:
        logging.debug("Recalculating error rate for each number of epocs")
        h, l = thisNN.search.getHiddenUnitsAndLearningRate()
        thisNN.search.calcEpocs(trainingSet, rangeEpocs, h, l)
        dumpNetwork = True

    if forceNN:
        search = thisNN.search
        thisNN = search.getBestNN(trainingSet, 0.0001)
        thisNN.search = search
        dumpNetwork = True
        
    if trainingError:
        print "Training Error:",thisNN.validate(trainingSet)[0]
    
    if dumpNetwork:
        file = open(saveFilePath,'w')
        cPickle.dump(thisNN, file)
        file.close()
        logging.debug("NN saved to: %s"% (saveFilePath))

    
