#!/usr/bin/python
from random import uniform as _uniform, shuffle as _shuffle, seed as _seed
from math import exp as _exp, log as _log
from sys import maxint as _MAXINT



#A bunch of math functions used by the NN
#Scalar functions
def _sigmoid(x):
    """Sigmoid function
    
    >>> _sigmoid(0)
    0.5
    >>> _sigmoid(1)
    0.7310585786300049
    >>> _sigmoid(-1)
    0.2689414213699951
    """
    e=0
    try:
        e = _exp(-1*x)
    except OverflowError:
        return 0
    return 1./(1.+e)

#Vector functions

def _checkSize(X1,X2):
    """Makes sure that both lists (X1,X2) are the same length
    
    >>> _checkSize([1],[0])
    >>> _checkSize([1],[])
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
      File "<stdin>", line 5, in _checkSize
    ValueError: Lists are differnt lengths
    """
    
    if len(X1) != len(X2):
        raise ValueError, 'Lists are differnt lengths'


def _mulVectors(X1,X2):
    """Returns the dot product of 2 lists
    
    >>> _mulVectors([1,2,3],[1,2,3])
    14
    """
    _checkSize(X1,X2)
    return sum([ X1[i] * X2[i] for i in range(len(X1))])
    
def _subVectors(X1,X2):
    """Returns the difference of two lists 
    
    >>> _subVectors([1,2,3],[1,2,3])
    [0, 0, 0]
    """
    _checkSize(X1,X2)
    return [ X1[i] - X2[i] for i in range(len(X1))]
    
def _addVectors(X1,X2):
    """Returns the addition of two lists 
    
    >>> _addVectors([1,2,3],[1,2,3])
    [2, 4, 6]
    """
    _checkSize(X1,X2)
    return [ X1[i] + X2[i] for i in range(len(X1))]
    
def _addMats(X1,X2):
    """Returns the addition of two lists of lists
    
    >>> W = [[d for d in range(5)] for h in range(5)]
    >>> V = [[d*2 for d in range(5)] for h in range(5)]
    >>> _addMats(W,V)
    [[0, 3, 6, 9, 12], [0, 3, 6, 9, 12], [0, 3, 6, 9, 12], [0, 3, 6, 9, 12], [0, 3, 6, 9, 12]]
    """
    _checkSize(X1,X2)
    return [ _addVectors(X1[i],X2[i]) for i in range(len(X1))]  
    
def _scalorTimesVectors(S,X):
    """Returns multiplication the scalor(S) and the list(X)
    
    >>> _scalorTimesVectors(10,[1,2,3])
    [10, 20, 30]
    """
    return [ S * x for x in X]

class NeuralNetwork:
    """An implementation of Alpaydin's neural network psudeo-code
    Currently only works with numeric inputs 
        
    >>> from random import seed
    >>> from ML1050.TrainingSet import TrainingSet
    >>> from ML1050.Example import LabeledExample
    >>> from ML1050.Classifiers.NeuralNetwork import NeuralNetwork
    
    Seed the RNG so we get the same network everytime for testing 
    >>> seed(0)
    
    Create the network and training sets
    >>> myNN = NeuralNetwork(   inputs = 2, \
                                outputs = 1, \
                                hiddenUnits = 2, \
                                learningRate=0.4, \
                                momentumRate=0.85 \
                            )


    >>> trainingSet = TrainingSet()
    >>> trainingSet.append(LabeledExample([1,1], label = [1]))
    >>> trainingSet.append(LabeledExample([0,1], label = [0]))
    >>> trainingSet.append(LabeledExample([1,0], label = [0]))
    >>> trainingSet.append(LabeledExample([0,0], label = [0]))
        
        
    Train the network for 100 Epocs
    >>> myNN.train(trainingSet,100)
    >>> answer = myNN.validate(trainingSet)
    >>> print "%.5f" % (answer[0])
    0.08375
    
    """
    def __init__(self, 
                inputs, 
                outputs, 
                hiddenUnits, 
                learningRate=0.3, 
                momentumRate=0., 
                regression=True,
                adaptiveLearning=False,
                adaptiveHistory=5,
                adaptiveAlpha=0.05,
                adaptiveBeta=2.0):
        """
        inputs - number of input this NN has
        outputs - number of outputs this NN has
        hiddenUnits - number of hiddenUnits to use in this NN
        learningRate - size of step in error space
        momentumRate - if momentumRate > 0 then steps in error space will 
                        have momentum from preivous epocs
        regression - if False assume a classification network and 
                        apply softmax function to outputs before 
                        they are returned
        adaptiveLearning - if True, backpropagation will use an adaptive 
                        learning rate.  The initial rate will be the 
                        value from learningRate
        adaptiveHistory - number of epochs to determine average error to
                        set learningRate
        adaptiveAlpha - if the average error rate decreases, learning 
                        rate will increase by this amount
        adaptiveBeta - if the average error rate increases, learning rate
                        will decrease by a factor of this value
        """
        
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
        self.regression = regression

        
        #Init V(hidden layer to output layer weights)  to small random numbers
        self.V = [[_uniform(-1,1)/100. for h in range(self.H)] \
                    for k in range(self.K)]
        
        
        #Init W(intput layer to hidden layer weights) to small random numbers
        self.W = [[_uniform(-1,1)/100. for d in range(self.D)] \
                    for h in range(self.H-1)]
            
        #Init last step to 0
        self.lastDeltaW = [[0 for d in range(self.D)] for h in range(self.H)]


    def _transformEx(self,example):
        """Transform and ML1050.Example into 2 lists
        """
        x = []
        x.extend(example)   
        x.append(1)
        return x,example.label
    
    def _propagateInput(self, input):
        if self.regression:
            return self._propagateInputRegression(input)
        else:
            return self._propagateInputClassification(input)

    def _propagateInputRegression(self,input):
        """Move input through network; return Y(output values) 
            and Z(hidden layer values)
        """
        Y = [0] * self.K #init output to list of K zeroes
            
        #init hidden layer to list of 1 followed by H zeroes
        Z = [0] * (self.H -1) 
            
        #propagate inputs to hidden layer (start at 1, 
        #first node in hidden layer should not be touched)
        for h in range(0,self.H-1):
            #Z = sig(W^T * x)           
            Z[h] = _sigmoid(_mulVectors(self.W[h],input))
            
        Z.append(1)     
            
        #propagate hidden layer to outputs
        for i in range(0,self.K):
            #y = v^T * z
            Y[i] = _mulVectors(self.V[i],Z)
            
        return Y,Z
    
    def _propagateInputClassification(self,input):
        """Same as _propagateInput; but applies softMax
        """
        Y,Z = self._propagateInputRegression(input)
            
        #apply softmax function
        try:
        
            expY = [_exp(y) for y in Y]
          
        #if the exp of the outputs starts getting too big just normalize the outputs
        except OverflowError: 
            expY = Y
        sumExpY = sum(expY)
 
        Y = [y/sumExpY for y in Y]
        
        return Y,Z
    
    def train(self, trainingSet, epochs=1, errorMin=0): 
        """ Trains the neural network from a training set using
            backpropgation algorithm from pg 251 of Alpaydin
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
                
                 
                    scalar = self.lRate * sumError * Z[h] * (1 - Z[h])

                    wh = _scalorTimesVectors(scalar, x)
                
                    #now calc momentum
                    momentum = _scalorTimesVectors(self.mRate,self.lastDeltaW[h])
                
                    deltaW.append(_addVectors(wh,momentum))             
    
                #save deltaW for next iters momentum
                self.lastDeltaW = deltaW

                #apply changes to weights
                self.V = _addMats(self.V,deltaV)
                self.W = _addMats(self.W,deltaW)
            
            error = self.validate(trainingSet)[0]
            #if errorMin is 0 don't waste time validating
            if errorMin != 0 and error <= errorMin:
                return
            
            if self.aLearning:
                self._updateLearningRate(error)


            
    def _updateLearningRate(self, error):
        
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

            
    def __repr__(self):
        """Print the weights in the network"""
        output = ""
        output +="V:\n"
        for row in self.V:
            output += "\t"
            for el in row:
                output += str(el) + " " 
            output += "\n"  
            
        output += "\nW:\n"
        for row in self.W:
            output += "\t"
            for el in row:
                output += str(el) + " " 
            output += "\n"
        return output 
        
    def test(self, example):
        """Test an example; will return Y output vector"""
        #just get input; don't care about class label
        x = self._transformEx(example)[0] 
        Y = self._propagateInput(x)[0]
        
        return Y
        

    def validate(self, trainingSet):
        """Test an entire training set; 
            For regression return sum squared error, 
            For regression return the % wrong
        """ 
        if self.regression:
            return self._validateRegression(trainingSet)          
        else:
            return self._validateClassification(trainingSet)

    def _validateClassification(self, trainingSet):
        """Test an entire training set and return the % wrong"""
        wrongCount = 0.

        pv = []
        tv = []

        if self.K == 1:
            for example in  trainingSet:
                Y = self.test(example)
                
                givenClass = example.label[0]
                if Y[0] < 0.5:
                    chosenClass = 0
                else:
                    chosenClass = 1
                
                pv.append(chosenClass)
                tv.append(givenClass)
                
                if chosenClass != givenClass:
                    wrongCount += 1.
        else:
            for example in  trainingSet:
                Y = self.test(example)
                
                posterior, chosenClass = max((x, i) for i, x in enumerate(Y))
                max_val, givenClass = max((x, i) for i, x in enumerate(example.label))
                
                pv.append(chosenClass)
                tv.append(givenClass)
    			
                if chosenClass != givenClass:
                    wrongCount += 1.
                
        return wrongCount/len(trainingSet), pv, tv
        
    def _validateRegression(self, trainingSet):
        """Error = 0.5 * 
                (sum all training examples ,t 
                    (sum all outputs ,i 
                        (output(t,i) - label(t,i))^2 ))"""
        
        sumErrors = [0] * len(trainingSet[0].label)               

        sumTotal = 0
        
        for example in trainingSet:
            Y = self.test(example)
            
            errors = [(example.label[i] - Y[i])**2 for i in range(0,self.K)]
            
            for i in range(len(errors)):
                sumErrors[i] += errors[i]
                
            sumTotal += sum(errors) 
                        
        return 0.5 * sumTotal, errors
    
    def __call__(self, example):
        """
        Calling an instance like a function is used to test a new example. 
        """
        return self.test(example)


    
def _test():
    """Run the tests in the documentation strings."""
    import doctest
    return doctest.testmod(verbose=True)
    
if __name__ == "__main__":
    try:
        __IP                            # Are we running IPython?
    except NameError:
        _test()                         # If not, run the tests