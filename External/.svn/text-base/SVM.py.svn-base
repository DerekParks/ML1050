from ML1050.External.libsvm285.python.svm import *
from math import log
from ML1050.Utils.StringMap import StringMapper
from math import exp
from ML1050.Example import LabeledExample
from ML1050.TrainingSet import TrainingSet
import types
import copy

class SVM:
    '''
    >>> from ML1050.External.SVM import SVM
    >>> from ML1050.TrainingSet import TrainingSet
    >>> from ML1050.Example import LabeledExample
    >>> m = SVM()
    >>> t = TrainingSet('Datasets/NBA_TRAIN.csv')
    >>> m.train(t)
    >>> ex = LabeledExample([None,2.050,230])
    >>> print m.test(ex)
    2
    >>> t = TrainingSet('Datasets/votes-train0.csv')
    >>> m.train(t)
    >>> ex = LabeledExample([None,'n','y','n','n','y','y','n','n','n','n','y','n','y','y','n','y'])
    >>> m.test(ex)
    'D'
    '''
    def __init__(self, kernelType = 'RBF', svm_type = 'C_SVC', degree = 3, gamma = 0, \
                coef0 = 0, nu = 0.5, cache_size = 40, C = 1, eps = '1e-3', p = 0.1, \
                shrinking = 1, probability = 1):
        """
        here you can set the kernel type, and anything else that 
        might need to be added in the future
        """
        
        self.par = svm_parameter(kernel_type = getattr(svmc,kernelType))
        self.par.svm_type = getattr(svmc,svm_type)
        self.par.degree = int(degree)
        self.par.gamma = float(gamma)
        self.par.coef0 = float(coef0)
        self.par.nu = float(nu)
        self.par.cache_size = float(cache_size)
        self.par.C = float(C)
        self.par.eps = float(eps)
        self.par.p = float(p)
        self.par.shrinking = int(shrinking)
        self.par.probability = int(probability)
        self.packParams = { "kt" : self.par.kernel_type, "st" : self.par.svm_type,\
                            "degree" : self.par.degree, "gamma" : self.par.gamma,\
                            "coef" : self.par.coef0, "nu" : self.par.nu,\
                            "cache" : self.par.cache_size, "C" : self.par.C,\
                            "eps" : self.par.eps, "p" : self.par.p,\
                            "shrink" : self.par.shrinking, "prob" : self.par.probability}
        
    def train(self, trainingSet):
        '''
        Train a model using a given training set
        '''
        self.strmap = StringMapper(trainingSet)
        self.trainingSet = trainingSet
        """
        ensure we are only working with numbers
        """
        labels = []
        data = []
        
        for example in trainingSet:
            mappedExample = self.strmap.map(example)
            labels.append(mappedExample.label)
            data.append(mappedExample[:])
        SVMtrain = svm_problem(labels, data)
        #print labels,data
        # here's the model:
        self.m = svm_model(SVMtrain, self.par)

    def save(self,fileName = "SvmModel.svm"):
        '''
        Save the state of the model object.
        '''
        import cPickle
        file = open(fileName,'w')
        params = (self.packParams,self.trainingSet)
        cPickle.dump(params,file)
        
        
    def load(self,fileName = "SvmModel.svm"):
        '''
        Load a previously saved SVM model.
        '''
        import cPickle
        file = open(fileName,'r')
        params = None
        try:
            params = cPickle.load(file)
            self.packParams = params[0]
            self.trainingSet = params[1]
        except :
            print fileName,": Not a valid svm model"
            
        self.par = svm_parameter(kernel_type = params[0]['kt'])
        self.par.svm_type = params[0]['st']
        self.par.degree = params[0]['degree']
        self.par.gamma = params[0]['gamma']
        self.par.coef0 = params[0]['coef']
        self.par.nu = params[0]['nu']
        self.par.cache_size = params[0]['cache']
        self.par.C = params[0]['C']
        self.par.eps = params[0]['eps']
        self.par.p = params[0]['p']
        self.par.shrinking = params[0]['shrink']
        self.par.probability = params[0]['prob']
        #self.packParams = { "kt" : self.par.kernel_type, "st" : self.par.svm_type,\
                            #"degree" : self.par.degree, "gamma" : self.par.gamma,\
                            #"coef" : self.par.coef0, "nu" : self.par.nu,\
                            #"cache" : self.par.cache_size, "C" : self.par.C,\
                            #"eps" : self.par.eps, "p" : self.par.p,\
                            #"shrink" : self.par.shrinking, "prop" : self.par.probability}
            
        
        self.train(self.trainingSet)

    def test(self, example):
        '''
        Get classification of a single example
        '''
        mappedExample = self.strmap.map(example)
        ret = self.m.predict(mappedExample[:])
        return self.strmap.revMapLabel(ret)
        
    def prob(self, example):
        """
        Get the probability of belonging to a class
        returns predicted class and list of probabilities indexed
            by class

        >>> from ML1050.External.SVM import SVM
        >>> from ML1050.TrainingSet import TrainingSet
        >>> from ML1050.Example import LabeledExample
        >>> m = SVM()
        >>> t = TrainingSet('Datasets/votes-train0.csv')
        >>> m.train(t)
        >>> ex = LabeledExample([None,'n','y','n','n','y','y','n','n','n','n','y','n','y','y','n','y'])
        >>> m.prob(ex)
        (0.0, {0: 0.97859933273907052, 1: 0.021400667260929488})
        """
        mappedExample = self.strmap.map(example)
        ret = None
        try:
            prd, ret = self.m.predict_probability(mappedExample[:])
            return prd, ret
        except TypeError:
            print "Model cannot extract probability"



    def __call__(self, example):
        return self.test(example)

"""
class StringMapper:
    def __init__(self, referenceSet):
        self.labelMap = {}
        self.labelCount = 0
        self.attributeMap = [None]*len(referenceSet[0])
        self.attributeCount = [0]*len(referenceSet[0])
        #check all attributes, and lets find the ones that need numberification
        self.doMap = [x for x in range(len(referenceSet[0])) if self.stringTest(referenceSet[0][x]) == True]
        self.doLabel = self.stringTest(referenceSet[0].label)
        
        
        
        self.set = True
        
        for index in self.doMap:
            self.attributeMap[index] = {}
        
        #trapdoor. we dont need to do all this work, if the data is fine as is
        if self.doLabel == False and sum(self.doMap) == 0:
            self.set = False
            return
        
        #translate em all
        for element in referenceSet:
            #check the label
            if self.doLabel:
                if self.conditionalDictAdd(self.labelMap,element.label,self.labelCount):
                    self.labelCount += 1
            for index in self.doMap:
                if self.conditionalDictAdd(self.attributeMap[index],element[index],self.attributeCount[index]):
                    self.attributeCount[index] += 1
        #print self.labelMap,self.attributeMap
        
    def map(self,input):
        if self.set:
            #return new label
            if (input.label == None):
                newLabel = None
            else:
                if self.conditionalDictAdd(self.labelMap,input.label,self.labelCount):
                    self.labelCount += 1
                newLabel = self.labelMap[input.label]
            newData = input[:]
            for index in self.doMap:
                if self.conditionalDictAdd(self.attributeMap[index],newData[index],self.attributeCount[index]):
                    self.attributeCount[index] += 1
                newData[index]=self.attributeMap[index][input[index]]
            ex = LabeledExample(newData,label=newLabel)
            return ex       
        else:
            #sanitize
            ex = LabeledExample([self.convertToNative(x) for x in input[:]],label=self.convertToNative(input.label))
            return ex

    def revMapLabel(self,input):
        if self.set:
            return self.labelMap.keys()[self.labelMap.values().index(int(input))]
        else:
            return input
        
    def conditionalDictAdd(self,hashtable,key,value):
        if not hashtable.has_key(key):
            hashtable[key]=value
            return True
        return False
        
            
    def stringTest(self,object):
        try:
            float(object)
            #it is a num
            return False
        except ValueError:
            #sneaky string
            return True
    def convertToNative(self,object):
        if object == None:
            return None
        try:
            return int(object)
        except ValueError:
            try:
                return float(object)
            except ValueError:
                #if you get here, something is bad.
                return object
            
            """

def _test():
    import doctest
    return doctest.testmod(verbose=True)

if __name__ == "__main__":
    try:
        __IP
    except NameError:
        _test()
