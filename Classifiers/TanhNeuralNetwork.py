from random import uniform as _uniform, shuffle as _shuffle, seed as _seed
from math import exp as _exp, log as _log, tanh as _tanh
from sys import maxint as _MAXINT
from ML1050.Classifiers.NeuralNetwork import _mulVectors, _checkSize, \
    _subVectors, _addVectors, _addMats, _scalorTimesVectors
from ML1050.Preprocessing import NNPreprocessing
from ML1050.Utils.ConfusionMatrix import ConfusionMatrix
from ML1050.TrainingSet import TrainingSet
from ML1050.Example import LabeledExample
import cPickle



class TanhNeuralNetwork:
    """
    This is a neural network that uses the hyperbolic tangent as an activation function.
    
    The constrctor takes multuple inputs, several of which have default values set.
    
    The required inputs are:
       NNPreproc - the preprocessor used to process the data
       inputs - number of input this NN has
       outputs - number of outputs this NN has
       
    The optional inputs are:
       learningRate (default = 0.3)- size of step in error space
       momentumRate (default = 0)- if momentumRate > 0 then steps in error space will 
                       have momentum from preivous epocs
       adaptiveLearning (default = False)- if True, backpropagation will use an adaptive 
                       learning rate.  The initial rate will be the 
                       value from learningRate
       adaptiveHistory (default = 5)- number of epochs to determine average error to
                       set learningRate
       adaptiveAlpha - (default = 0.05) if the average error rate decreases, learning 
                       rate will increase by this amount
       adaptiveBeta - (default = 2.0) if the average error rate increases, learning rate
                       will decrease by a factor of this value
    
    >>> from ML1050.TrainingSet import TrainingSet
    >>> from ML1050.Example import LabeledExample
    >>> from ML1050.Classifiers.TanhNeuralNetwork import TanhNeuralNetwork
    >>> from ML1050.Preprocessing.NNPreprocessing import NNPreprocessing
    >>> from random import seed
    >>> from ML1050.Utils.ConfusionMatrix import ConfusionMatrix
    
    for testing
    >>> seed(0)
    
    start with a simple training set
    >>> trainingSet = TrainingSet()
    >>> trainingSet.append(LabeledExample(['t', 1.0, 0.0]))
    >>> trainingSet.append(LabeledExample(['t', 0.0, 1.0]))
    >>> trainingSet.append(LabeledExample(['f', 1.0, 1.0]))
    >>> trainingSet.append(LabeledExample(['f', 0.0, 0.0]))
    
    preprocessing is required
    >>> preProcessor = NNPreprocessing(trainingSet)
    
    create a simple NN
    >>> simpleNN = TanhNeuralNetwork(NNPreproc = preProcessor, \
                                     inputs = len(trainingSet[0]), \
                                     outputs = len(trainingSet[0].label), \
                                     hiddenUnits = 1)
                                  
                                 
    Here is a sample process to train a more complex NN 
    >>> complexNN = TanhNeuralNetwork(NNPreproc = preProcessor, \
                                      inputs = len(trainingSet[0]), \
                                      outputs = len(trainingSet[0].label), \
                                      hiddenUnits = 2, \
                                      learningRate = 0.01, \
                                      momentumRate = 0.001, \
                                      adaptiveLearning = True, \
                                      adaptiveHistory = 3, \
                                      adaptiveAlpha = 0.005, \
                                      adaptiveBeta = 1.5)
    >>> epochs = 10
    >>> complexNN.train(trainingSet, epochs)
    
    Getting the error is useful when trying different parameters
    No translation is needed since we are using the preprocessed training set in 
    this example
    >>> error = complexNN.validate(trainingSet, translate = False)
    >>> print '%.5f' % error
    0.50000
    
    The classify function is used to get a class label for an unknown example
    If a preprocessed example is given to the function the translate prameter must 
    be set to False.  The default value is true.
    >>> ex = LabeledExample(trainingSet[0][:], label = trainingSet[0].label)
    >>> print complexNN.classify(ex, translate = False)
    [0]
    
    For a non preprocessed example
    >>> ex = LabeledExample(['t', 1.0, 0.0])
    >>> print complexNN.classify(ex)
    t
    
    Here is anoter example. Obviously, this is a poorly trained network.
    >>> ex = LabeledExample(['f', 0.0, 0.0])
    >>> print complexNN.classify(ex)
    t
    
    The test function will test on an entire test set and return a Confusion Matrix
    This test needs to set translate to False, as it was preprocessed
    >>> cm = complexNN.test(trainingSet, translate = False)
    >>> cm.display()
             [0]      [1]      
    [0]      2        0        
    [1]      2        0        
    ==========================================
    Correctly classified:   2   
    Incorrectly classified:   2   
    Successfully classified:    50.00   %   
    
    
    You can also test with unprocessed test sets
    >>> testSet = TrainingSet()
    >>> testSet.append(LabeledExample(['t', 1.0, 0.0]))
    >>> testSet.append(LabeledExample(['t', 0.0, 1.0]))
    >>> testSet.append(LabeledExample(['f', 1.0, 1.0]))
    >>> testSet.append(LabeledExample(['f', 0.0, 0.0]))
    >>> cm = complexNN.test(testSet)
    >>> cm.display()
           t      f      
    t      2      0      
    f      2      0      
    ==========================================
    Correctly classified:   2   
    Incorrectly classified:   2   
    Successfully classified:    50.00   %   
    
    
    """

    def __init__(self,
                NNPreproc, 
                inputs, 
                outputs, 
                hiddenUnits, 
                learningRate=0.3, 
                momentumRate=0., 
                adaptiveLearning=False,
                adaptiveHistory=5,
                adaptiveAlpha=0.05,
                adaptiveBeta=2.0):
        
        if inputs < 1:
            raise ValueError, 'Network must have at least one input'
        
        if outputs < 1:
            raise ValueError, 'Network must have at least one output'
            
        if hiddenUnits < 1:
            raise ValueError, 'Network must have at least one hidden unit'
        
        if learningRate <= 0:
            raise ValueError, 'Learning rate must be above 0'
        
        if momentumRate < 0:
            raise ValueError, 'Momentum rate must be at least 0'
        
        
        self.H = hiddenUnits + 1 #need to have plus 1 for 1 in hidden layer
        self.K = outputs
        self.D = inputs + 1 #need to have plus 1 for 1 in input vector
        self.lRate = learningRate
        self.mRate = momentumRate
        self.aLearning = adaptiveLearning
        self.aHistory = adaptiveHistory
        self.aAlpha = adaptiveAlpha
        self.aBeta = adaptiveBeta
        self.aErrors = []
        self.o = []
        self.tanhMultiplier = 3.4318/3.
        self.NNPreproc = NNPreproc

        
        #Init V(hidden layer to output layer weights)  to small random numbers
        self.V = [[_uniform(-1,1)/100. for h in range(self.H)] \
                    for k in range(self.K)]
        
        
        #Init W(intput layer to hidden layer weights) to small random numbers
        self.W = [[_uniform(-1,1)/100. for d in range(self.D)] \
                    for h in range(self.H-1)]
            
        #Init last step to 0
        self.lastDeltaW = [[0 for d in range(self.D)] for h in range(self.H)]

    def _propagateInput(self,input):
        """Move input through network; return Y(output values) 
            and Z(hidden layer values)
        """
        Y = [0] * self.K #init output to list of K zeroes
            
        #init hidden layer to list of 1 followed by H zeroes
        Z = [0] * (self.H -1) 
            
        #propagate inputs to hidden layer (start at 1, 
        #first node in hidden layer should not be touched)
        self.o = []
        for h in range(0,self.H-1):
            wtx = _mulVectors(self.W[h],input)
            scaledWtx = _tanh((2./3.) * wtx)
            Z[h] = 1.7159 * scaledWtx
            self.o.append(scaledWtx);
            
        Z.append(1)     
            
        #propagate hidden layer to outputs
        for i in range(0,self.K):
            Y[i] = _mulVectors(self.V[i],Z)
            
        if len(Y) > 1:
            Y = self._softMax(Y)
                    
        return Y,Z
        
    def _updateLearningRate(self, error):
        """updates the learning rate if adaptive learning is active"""

        if len(self.aErrors) == 0:
            self.aErrors.append(error)
            return

        #calculate old and new average error
        Et = sum(self.aErrors)
        EtT = Et + error

        Et = Et/len(self.aErrors)
        EtT = EtT/(len(self.aErrors) + 1)

        #add new error to history
        self.aErrors.append(error)
        #if history is larger than specified value, pop off head
        if len(self.aErrors) > self.aHistory:
            self.aErrors.pop(0)

        if EtT <= Et:
            #if average error decreased, increase learning rate
            self.lRate += self.aAlpha
        else:
            #otherwise decrease rate geometrically
            self.lRate /= self.aBeta
        
    def _softMax(self,Y):
        """ softmax function used on outputs"""
        y = []
        sumExpY = 0.0
        for i in Y:
            sumExpY = sumExpY + _exp(i)
        for i in Y:
            t = _exp(i)/sumExpY
            y.append(t)
        return y
        
    def _transformEx(self,example):
        """Transform and ML1050.Example into 2 lists
        """
        x = []
        x.extend(example)   
        x.append(1)
        return x,example.label

        
    def validate(self, trainingSet, translate = True):
        """Test an entire training set and return the % wrong"""
        wrongCount = 0.
        for e in trainingSet:
            answer = self.classify(e, translate)
            if answer != e.label:
                wrongCount += 1
        return wrongCount/len(trainingSet)

    
    def train(self, trainingSet, epochs=1, errorMin=0): 
        """ Trains the neural network from a training set using
            backpropgation algorithm from pg 251 of Alpaydin
            
            epochs is the number of training passes
            errorMin is the threshold error value to stop training
            
            see the docstring for the TanhNeuralNetwork for an example
        """
    
        if epochs < 1:
            raise ValueError, 'epochs must be at least 1'
    
        if errorMin < 0:
            raise ValueError, 'errorMin must be greater or equal to than 0'
    
        for epoch in range(epochs):
            
            #Should run through the training set in random order
            _shuffle(trainingSet)
        
            for example in trainingSet:
                x,r = self._transformEx(example)            
                Y,Z = self._propagateInput(x)
            
                #Calc change in hidden to output weights
                deltaV = [_scalorTimesVectors(self.lRate * (r[i] - Y[i]) , Z) \
                   for i in range(self.K)]
            
                #Calc change in input to hidden weights
                deltaW = []
            
                for h in range(0,self.H -1):
                    sumError = sum([((r[i] - Y[i]) * self.V[i][h]) \
                        for i in range(self.K)])
                
                 
                    #dz/dw = 3.4318/3(1-(tanh((2/3)wx))**2)x
                    scalar = self.lRate * sumError * self.tanhMultiplier * (1 - self.o[h]**2) 

                    wh = _scalorTimesVectors(scalar, x)
                
                    #now calc momentum
                    momentum = _scalorTimesVectors(self.mRate,self.lastDeltaW[h])
                
                    deltaW.append(_addVectors(wh,momentum))             
    
                #save deltaW for next iters momentum
                self.lastDeltaW = deltaW

                #apply changes to weights
                self.V = _addMats(self.V,deltaV)
                self.W = _addMats(self.W,deltaW)
            
            error = self.validate(trainingSet, translate = False)
            #if errorMin is 0 don't waste time validating
            if errorMin != 0 and error <= errorMin:
                return
            
            if self.aLearning:
                self._updateLearningRate(error)
    
    def classify(self, example, translate = True):
        """given an example, outputs the class label determined by the network
           If the example is preprocessed, translate must be set to False
           
           see the TanhNerualNetwork docstring for an example
        """
        myExample = None
        ts = None
        if translate == True:
            # example provided needs to be changed into the NN format
            myExample = LabeledExample(example[:], label = example.label)
            ts = TrainingSet()
            ts.append(myExample)
            self.NNPreproc.forward(ts)
            myExample = ts[0]
        else:
            myExample = example
        Y = self._test(myExample)
        rawAnswer=[]
        if len(Y) > 1:
            maxValue = 0.
            maxIndex = 0
            for i in range(len(Y)):
                if Y[i] > maxValue:
                    maxValue = Y[i]
                    maxIndex = i
                rawAnswer.append(0)
            rawAnswer[maxIndex] = 1
        else:
            if Y[0] < 0.5:
                rawAnswer.append(0)
            else:
                rawAnswer.append(1)
        if translate == True:
            myExample.label = rawAnswer
            self.NNPreproc.back(ts)
            return ts[0].label
        else:
            return rawAnswer
                
    def _test(self, example):
        """Test an example; will return Y output vector"""
        #just get input; don't care about class label
        x = self._transformEx(example)[0] 
        Y = self._propagateInput(x)[0]

        return Y
        
    def test(self, testSet, translate = True):
        """This will test against an entire training set and will output a Confusion matrix.
        If the data is already preprocessed, translate must be set to False.
        An example is provided the the TanhNeuralNetwork docstring
        """
        guessedClassifications = [] 
        trueClassifications = []
        for e in testSet:
            guessedClassifications.append(self.classify(e, translate))
            trueClassifications.append(e.label)
        return ConfusionMatrix(guessedClassifications, trueClassifications)
    
    def serialize(self, filename) :
        """Accepts a filename and saves classifier to that file.
        """
        outfile = open( filename, "wb")
        cPickle.dump( self, outfile)
        outfile.close()

def _test():
    """Run the tests in the documentation strings."""
    import doctest
    return doctest.testmod(verbose=True)

if __name__ == "__main__":
    try:
        __IP                            # Are we running IPython?
    except NameError:
        _test()                         # If not, run the tests