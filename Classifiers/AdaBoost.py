"""
Implementation of Adaboost based on T. Hastie, R. Tibshirani, J. Friedman's Adaboost.M1
"""

from math import log
from math import exp
from ML1050.Classifiers.DecisionTree import DecisionTree
from ML1050.Example import LabeledExample
from ML1050.TrainingSet import TrainingSet,createTrainingSet
from ML1050.Classifiers.Classifier import Classifier
#from itertools import izip

import types, copy, random

class AdaBoost(Classifier):
    """
    AdaBoost is a sweet algorithm for creating ensombles of classifiers.
    It has many advantages. For example, even when training error becomes
    zero, more classifiers can continue to lower test error.
    
    Here is how to use AdaBoost:
    First, import AdaBoost, the classifier you want to boost,
    trainingSet and LabeledExample for testing.
    >>> from Classifiers import AdaBoost
    >>> from ML1050.Classifiers.DecisionTree import DecisionTree
    >>> from ML1050.Example import LabeledExample
    >>> from ML1050.TrainingSet import TrainingSet
    
    Load your training set:
    >>> ts = TrainingSet('Datasets/votes-train0.csv')
    
    Create an instance of the classifier with the parameters you want
    >>> tree = DecisionTree(maxDepth=1)
    
    Pass that into AdaBoost, with the number of models you want to make (M).
    >>> ab = AdaBoost.AdaBoost(tree,M=2)
    
    Train AdaBoost
    >>> ab.train(ts)
    
    Then test to your heart's content
    >>> testExample = LabeledExample([None, 'n','y','n','n','y','y','n','n','n','n','y','n','y','y','n','y'])
    >>> ab.test(testExample)
    'D'
    """
    def __init__(self, classifier=None, M = 10, classifierArgs=[], preConstructedClassifier = True):
        ''' 
        Take the given classifier and create M models
        '''
        self.g = [None]*M
        self.a = [None]*M
        self.M = M
        self.charmap = OutputMap()
        if classifier == None:
            #use default in decision stump
            for i in range(M):
                self.g[i] = DecisionTree(maxDepth=1)
        else:
            if preConstructedClassifier:
                #the user has already built the classifier. use it instead.
                for i in range(M):
                    self.g[i] = copy.copy(classifier)
            else:
                #the classifier is not constructed.
                for i in range(M):
                    self.g[i] = classifier(*classifierArgs)
    def train(self,trainingSet,useSamples=False):
        if useSamples:
            print "Using sampled training set"
        self.useSamples = useSamples
        self.N = len(trainingSet)
        self.w = [1.0/self.N]*self.N
        #Initialize weights
        for i in range(self.N):
            self.charmap.load(trainingSet[i].label)
        #Iterate through all the models
        for m in range(self.M):
            #Train the model
            if useSamples:
                self.g[m].train(replacementSample(trainingSet,self.w,self.N))
            else:
                self.g[m].train(trainingSet,self.w)
                
            #Compute error
            err = self.err(self.g[m],trainingSet,self.w)
            
            #Compute model weight
            self.a[m] = log((1.0-float(err))/float(err))
            
            #Reweight
            self.reweight(trainingSet,m)
    def test(self, example):
        output = []
        for m in range(self.M):
            output.append(self.g[m].test(example))
        if self.charmap.anymapped():
            output = [self.charmap.map(x) for x in output]
        ssum = 0.0
        for m in range(self.M):
            # the problem here is that both outputs are positive!
            ssum += self.a[m]*float(output[m])
        if self.charmap.anymapped():
            return self.charmap.revmap(sign(ssum))
        else:
            return sign(ssum)
            
                
    def err(self,classifier, dataSet, modifier):
        indication = self.indicator(classifier, dataSet, modifier)
        indication /= sum(modifier)
        return indication
    
    def indicator(self,classifier, dataSet, modifier):
        compt = [ classifier.test(x) != x.label for x in dataSet]
        #print sum(compt),"++++"
        compt = [ modifier[i]*float(compt[i]) for i in range(len(compt))]
        return sum(compt)
    
    def reweight(self,trainingSet,m):
        compt = [ self.g[m].test(x) != x.label for x in trainingSet]
        self.w = [ self.w[i]*exp(float(compt[i])*self.a[m]) for i in range(len(compt))]
        normalf = sum(self.w)
        self.w = [ i/normalf for i in self.w]
            
    def __call__(self, example):
        return self.test(example)
def main():
    pass

class OutputMap():
    def __init__(self):
        self.neg = None
        self.pos = None
        self.set = False
    def load(self, object):
        #if self.checkString(object):
        if self.pos == None:
            self.pos = object
            return
        if self.neg == None and object != self.pos:
            self.neg = object
            return
    def map(self, object):
        if object == self.neg:
            return -1.0
        if object == self.pos:
            return 1.0
    def revmap(self, object):
        if object < 0.0:
            return self.neg
        if object > 0.0:
            return self.pos
    
    def outp(self):
        print "-1.0",self.neg,"1.0",self.pos
    def anymapped(self):
        return self.neg != None or self.pos != None
    def checkString(self, object):
        """check if a given input is a number or a string"""
        try:
            float(object)
            return False
        except ValueError:
            return True

def sign(x):
    """Function to aid final output"""
    if x < 0.0:
        return -1.0
    elif x > 0.0:
        return 1.0
    else:
        return 0.0
            
def convert(obj, ref):
    """Change a label to a double for calculating final output"""
    if obj == ref:
        return 1.0
    else:
        return -1.0

def replacementSample(dataset,weights, num):
    '''Sample, with replacement, from a given distribution, and return a new training set of a given size'''
    random.seed()
    sampledList = [None]*num
    for i in range(num):
        csum = 0.0
        threshHold = random.random()
        for j in range(len(weights)):
            csum += weights[j]
            if csum > threshHold:
                sampledList[i]=dataset[j]
                break
    return sampledList

    
def _test():
    import doctest
    return doctest.testmod(verbose=True)

if __name__ == "__main__":
    try:
        __IP
    except NameError:
        pass
        _test()
    main()
