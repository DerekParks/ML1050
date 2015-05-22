"""
ML1050.Utils.NNParameterSearch
3/15/08

This is a simple class that searches for the best number of hidden units, the best learning rate,
and the number of epocs to train a Neural Network. It is has simple graphing capabilities and can
create and train a Neural Network based on what it thinks are optimal parameters. 
"""

from ML1050.Classifiers.NeuralNetwork import NeuralNetwork
from ML1050.Preprocessing.CrossValidation import kFold
from pylab import rcParams, plot, xlabel, ylabel, legend, show, title
import logging

class NNParameterSearch:
    """
    >>> from ML1050.TrainingSet import TrainingSet
    >>> from ML1050.Example import LabeledExample
    >>> from random import seed
    
    Seed the RNG so we get the same network everytime for testing 
    >>> seed(0)
    
    >>> trainingSet = TrainingSet()
    >>> trainingSet.append(LabeledExample([1,1], label = [1]))
    >>> trainingSet.append(LabeledExample([0,1], label = [0]))
    >>> trainingSet.append(LabeledExample([1,0], label = [0]))
    >>> trainingSet.append(LabeledExample([0,0], label = [0]))
    >>> trainingSet.append(LabeledExample([1,1], label = [1]))
    >>> trainingSet.append(LabeledExample([0,1], label = [0]))
    >>> trainingSet.append(LabeledExample([1,0], label = [0]))
    >>> trainingSet.append(LabeledExample([0,0], label = [0]))
    >>> trainingSet.append(LabeledExample([1,1], label = [1]))
    >>> trainingSet.append(LabeledExample([0,1], label = [0]))
    >>> trainingSet.append(LabeledExample([1,0], label = [0]))
    >>> trainingSet.append(LabeledExample([0,0], label = [0]))
    
    >>> search = NNParameterSearch(2,1)
    >>> search.calcHL(trainingSet, [1,2], [.1,.2,.3,.4], 50)
    >>> search.getHiddenUnitsAndLearningRate()
    (2, 0.29999999999999999)
    >>> #search.graphHL(['r-', 'b-'])
    >>> h, l = search.getHiddenUnitsAndLearningRate()
    >>> search.calcEpocs(trainingSet, [1,10,25,50,75,100,200], h, l)
    >>> search.getEpocs()
    200
    >>> #search.graphEpocs()
    """
    
    _PRAMS = {'backend': 'ps',
               'axes.labelsize': 20,
               'text.fontsize': 20,
               'xtick.labelsize': 16,
               'ytick.labelsize': 16,
               'text.usetex': True,
               }
    
    def __init__(self, inputs, outputs, regression=True, k = 10, logLevel=logging.NOTSET):
        self.inputs = inputs
        self.outputs = outputs
        self.regression = regression
        self.k = k
        
        self.logLevel = logLevel
        self.errorsHL = None
        self.errorsEpocs = None
        self.rangeLearningRate = None

    def calcHL(self, trainingSet, rangeHiddenUnits, rangeLearningRate, epocs):
        """Calculate avg test k-fold error for all hidden unit and learning rate combinations"""
        logging.basicConfig(level=self.logLevel)
        self.errorsHL = []
        self.rangeHiddenUnits = rangeHiddenUnits
        self.rangeLearningRate = rangeLearningRate
        
        for h in rangeHiddenUnits:
            thisErrorsH = []
            for l in rangeLearningRate:
                thisErrorsH.append(self._getAvgTestErrorHL(trainingSet, h, l, epocs))
                logging.debug("Hidden Units %d, Learning Rate %.3f, Error %.5f" % (h,l,thisErrorsH[-1]))
            self.errorsHL.append(thisErrorsH)        


    def _getAvgTestErrorHL(self, trainingSet, hiddenUnits, learningRate, epocs):
        """Get the average k-fold test error for one hiddenUnit and learningRate"""
        avgTestError = [self._trainAndTestHL(training, validation, hiddenUnits, learningRate, epocs)
                                    for training, validation in kFold(trainingSet, self.k)]

        return sum(avgTestError)/self.k
        
    def _trainAndTestHL(self, training, test, hiddenUnits, learningRate, epocs):
        """Get test error for one fold for given hiddenUnits and learningRaate """
        myNN = NeuralNetwork(inputs = self.inputs, 
                             outputs = self.outputs, 
                             regression = self.regression,
                             hiddenUnits = hiddenUnits,
                             learningRate = learningRate)        
    
        myNN.train(training, epocs)
        
        return myNN.validate(test)[0]

    def getHiddenUnitsAndLearningRate(self):
        """Return number of hidden units and learning rate with min error"""
        
        minH = self.rangeHiddenUnits[0]
        minL = self.rangeLearningRate[0]
        minError = self.errorsHL[0][0]
        
        for i,h in enumerate(self.rangeHiddenUnits):
            for j,l in enumerate(self.rangeLearningRate):
                if minError > self.errorsHL[i][j]:
                    minError = self.errorsHL[i][j]
                    minH = h
                    minL = l
        return minH, minL

    def graphHL(self, styles):
        """ 
        Use matplotlib to plot error rates. styles is a list of line styles. Length of styles needs to be 
        equal to length of rangeHiddenUnits (One for every level of hidden units tested).
        """
        if self.rangeLearningRate == None or self.errorsHL == None:
            raise ValueError, 'Must call calcHAndL before calling  graphHL' 
        
        if len(styles) < len(self.rangeHiddenUnits):
            raise ValueError, 'Must have one style for every level of hidden units tested' 
        
        rcParams.update(self._PRAMS)

        for i,h in enumerate(self.rangeHiddenUnits):
            plot(self.rangeLearningRate, self.errorsHL[i], styles[i], label="h="+str(h), linewidth=2)

        xlabel('Learning Rate')
        ylabel('Error')
        title('Error for Hidden Units and Learning Rate')
        legend()
        show()

    def calcEpocs(self, trainingSet, epocsRange, hiddenUnits, learningRate):
        """
        Calculate the k-fold train and test error for every epoc in epocsRange at the given
        hiddenUnits and learningRate
        """
        logging.basicConfig(level=self.logLevel)
        self.epocsRange = epocsRange
        self.epocsErrors = [[],[]]

        #find the addition epocs amount to train 
        epocsRangeDiffs =  [ self.epocsRange[0] ]
        epocsRangeDiffs.extend(
                               [self.epocsRange[i] - self.epocsRange[i-1] 
                                    for i in range(1,len(self.epocsRange))]
                               )
            
        #do kfold for each epoc value in epocsRange
        epocsErrorsNotAverage = []

        for training, test in kFold(trainingSet, self.k):

            myNN = NeuralNetwork(inputs = self.inputs, 
                             outputs = self.outputs, 
                             regression = self.regression,
                             hiddenUnits = hiddenUnits,
                             learningRate = learningRate)
            thisFoldErrors=[]
            for i in range(len(epocsRangeDiffs)):

                myNN.train(training, epocsRangeDiffs[i])
                thisFoldErrors.append((myNN.validate(training)[0] , myNN.validate(test)[0]))
                logging.debug("Epocs %.3f, Train Error %.5f, Test Error %.5f" % 
                                    (self.epocsRange[i], thisFoldErrors[-1][0], thisFoldErrors[-1][1]))
            
            epocsErrorsNotAverage.append(thisFoldErrors)
        
        
        for e in range(len(self.epocsRange)):
            self.epocsErrors[0].append(
                        sum([epocsErrorsNotAverage[f][e][0] for f in range(self.k)]) / self.k
                        )
            self.epocsErrors[1].append(
                        sum([epocsErrorsNotAverage[f][e][1] for f in range(self.k)]) / self.k
                        )
            logging.debug("Epocs %.3f, Avg Train Error %.5f, Avg Test Error %.5f" % 
                                    (self.epocsRange[e], self.epocsErrors[0][-1], self.epocsErrors[1][-1]))
    
    def getEpocs(self):
        """Find the number of epocs to use without overfitting"""
        indexOfMinError = min((n, i) for i, n in enumerate(self.epocsErrors[1]))[1]
        return self.epocsRange[indexOfMinError]
    
    def graphEpocs(self):
        """Graph the average k-fold training and test error for all tested epocs"""
        rcParams.update(self._PRAMS)

        plot(self.epocsRange, self.epocsErrors[0], 'r-', label="Training Error", linewidth=2)
        plot(self.epocsRange, self.epocsErrors[1], 'b-', label="Test Error", linewidth=2)
        xlabel('Number Epocs')
        ylabel('Error')
        title('Epocs vs Error')
        legend()
        show()
        
    def getBestNN(self, trainingSet, minError=0):
        """Get a Neural Network with the best hidden units and learning rate.
        Then train to the best number of epocs."""
        hUnits, lRate = self.getHiddenUnitsAndLearningRate()
        thisNN = NeuralNetwork(inputs = self.inputs, 
                             outputs = self.outputs, 
                             regression = self.regression,
                             hiddenUnits = hUnits,
                             learningRate = lRate)

        thisNN.train(trainingSet, self.getEpocs(), minError)
        return thisNN
    
def _test():
    """Run the tests in the documentation strings."""
    import doctest
    return doctest.testmod(verbose=True)
    
if __name__ == "__main__":
    try:
        __IP                            # Are we running IPython?
    except NameError:
        _test()                         # If not, run the tests