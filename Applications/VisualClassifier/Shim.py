import os
import wx
import cPickle
from pylab import *
from ML1050.TrainingSet import TrainingSet
from ML1050.External.SVM import SVM
from ML1050.TrainingSet import TrainingSet
from ML1050.Example import LabeledExample
from random import random


class Shim:
    Classifier = None
    def __init__(self):
        self.parameters = {}
        self.dataDependance = 0
    def setParameter(self, key, value):
        self.parameters[key][0] = value
    def construct(self):
        pass
    def writeToFile(self,filename):
        file = open(filename,"wb")
        cPickle.dump(self.Classifier,file)
    def get(self):
        return self.Classifier
    
class EmptyShim(Shim):
    def __init__(self):
        Shim.__init__(self)

class DecTreeShim(Shim):
    #Classifier = None
    def __init__(self):
        Shim.__init__(self)
        self.thold = 0.1
        self.mDepth = 5
        self.parameters['Threshhold']=[self.thold,FLOATSELECTOR,0,1,50]
        self.parameters['Maximum Tree Depth']=[self.mDepth,INTSELECTOR,1,100,51]
        
    def construct(self):
        from ML1050.Classifiers.DecisionTree import DecisionTree
        #print self.parameters['Threshhold'][0],self.parameters['Maximum Tree Depth'][0]
        self.Classifier = DecisionTree(self.parameters['Threshhold'][0], self.parameters['Maximum Tree Depth'][0])
class SVMShim(Shim):
    def __init__(self):
        Shim.__init__(self)
        self.parameters['Kernel Type']=["RBF",DROPSELECTOR,["LINEAR","POLY","RBF","Sigmoid"],[0,1,2,3],60]
        self.parameters['SVM Type']=["C_SVC",DROPSELECTOR,["C_SVC","NU_SVC","ONE_CLASS","EPSILON_SVR","NU_SVR"],[0,1,2,3,4],61]
        self.parameters['Degree']=[3,INTSELECTOR,1,100,62]
        self.parameters['Gamma']=[0,FLOATSELECTOR,0,100,63]
        self.parameters['Coef0']=[0,FLOATSELECTOR,0,100,64]
        self.parameters['NU']=[0.5,FLOATSELECTOR,0,100,65]
        self.parameters['Cache Size']=[40,INTSELECTOR,0,100,66]
        self.parameters['C']=[1,INTSELECTOR,1,100,67]
        self.parameters['EPS']=[1e-3,FLOATSELECTOR,0,100,68]
        self.parameters['P']=[0.1,FLOATSELECTOR,0,100,69]
        self.parameters['Shrinking']=[1,BOOLEAN,1,0,70]
        self.parameters['Probability']=[1,BOOLEAN,1,0,71]
    def writeToFile(self,filename):
        self.Classifier.save(filename)
    def construct(self):
        from ML1050.External.SVM import SVM
        #for k in self.parameters.keys():
            #print k, self.parameters[k][0]
        self.Classifier = SVM(kernelType = self.parameters['Kernel Type'][0],\
                svm_type = self.parameters['SVM Type'][0],\
                degree = self.parameters['Degree'][0],\
                gamma = self.parameters['Gamma'][0],\
                coef0 = self.parameters['Coef0'][0],\
                nu = self.parameters['NU'][0],\
                cache_size = self.parameters['Cache Size'][0],\
                C = self.parameters['C'][0],\
                eps = self.parameters['EPS'][0],\
                p = self.parameters['P'][0],\
                shrinking = self.parameters['Shrinking'][0],\
                probability = self.parameters['Probability'][0])
                
class AdaBoostShim(Shim):
    def __init__(self):
        Shim.__init__(self)
        self.parameters['Classifier'] = [None, CLASSIFIERSELECTOR,0,0,300]
        self.parameters['Number of Models'] = [10, INTSELECTOR,1,500,301]
        self.parameters['Use Sampling'] = [0, BOOLEAN, 0,0,302]
    def construct(self):
        from ML1050.Classifiers.AdaBoost import AdaBoost
        self.Classifier = AdaBoost(self.parameters['Classifier'][0],self.parameters['Number of Models'][0])
        
class KNNShim(Shim):
    def __init__(self):
        Shim.__init__(self)
        self.parameters['Mode']=[0,INTSELECTOR,0,5,200]
        self.parameters['Distance Function']=[None, TEXT, 0, 0, 201]
        
class NNShim(Shim):
    def __init__(self):
        Shim.__init__(self)
        self.parameters['Number Inputs'] = [2,INTSELECTOR,1,100,80]
        self.parameters['Number Output '] = [1,INTSELECTOR,1,100,81]
        self.parameters['Hidden Units'] = [2,INTSELECTOR,1,100,82]
        self.parameters['Learning Rate'] = [0.4,FLOATSELECTOR,0.001,1.0,83]
        self.parameters['Momentum Rate'] = [0.85,FLOATSELECTOR,0.001,1.0,84]
        self.parameters['Regression'] = [1,BOOLEAN,1,0,85]
        self.parameters['Adaptive Learning'] = [0,BOOLEAN,0,0,86]
        self.parameters['Adaptive History'] = [5,INTSELECTOR,1,100,87]
        self.parameters['Adaptive Alpha'] = [0.05,FLOATSELECTOR,0.001,1.0,88]
        self.parameters['Adaptive Beta'] = [2.0,FLOATSELECTOR,0.001,10.0,89]
    def construct(self):
        from ML1050.Classifiers.NeuralNetwork import NeuralNetwork
        self.Classifier = NeuralNetwork(inputs = self.parameters['Number Inputs'][0],\
                outputs = self.parameters['Number Output '][0],\
                hiddenUnits = self.parameters['Hidden Units'][0],\
                learningRate = self.parameters['Learning Rate'][0],\
                momentumRate = self.parameters['Momentum Rate'][0],\
                regression = self.parameters['Regression'][0],\
                adaptiveLearning = self.parameters['Adaptive Learning'][0],\
                adaptiveHistory = self.parameters['Adaptive History'][0],\
                adaptiveAlpha = self.parameters['Adaptive Alpha'][0],\
                adaptiveBeta = self.parameters['Adaptive Beta'][0])
                
class TanhNNShim(Shim):
    def __init__(self):
        Shim.__init__(self)
        self.parameters['Number Inputs'] = [2,INTSELECTOR,1,100,90]
        self.parameters['Number Output '] = [1,INTSELECTOR,1,100,91]
        self.parameters['Hidden Units'] = [2,INTSELECTOR,1,100,92]
        self.parameters['Learning Rate'] = [0.4,FLOATSELECTOR,0.001,1.0,93]
        self.parameters['Momentum Rate'] = [0.85,FLOATSELECTOR,0.001,1.0,94]
        self.parameters['Regression'] = [1,BOOLEAN,1,0,95]
        self.parameters['Adaptive Learning'] = [0,BOOLEAN,0,0,96]
        self.parameters['Adaptive History'] = [5,INTSELECTOR,1,100,97]
        self.parameters['Adaptive Alpha'] = [0.05,FLOATSELECTOR,0.001,1.0,98]
        self.parameters['Adaptive Beta'] = [2.0,FLOATSELECTOR,0.001,10.0,99]
        
    def construct(self):
        from ML1050.Classifiers.TanhNeuralNetwork import TanhNeuralNetwork
        from ML1050.Preprocessing.NNPreprocessing import NNPreprocessing
        
        #preprocessor = need to find a way to load this at run time
        
        self.Classifier = NeuralNetwork(inputs = self.parameters['Number Inputs'][0],\
                outputs = self.parameters['Number Output '][0],\
                hiddenUnits = self.parameters['Hidden Units'][0],\
                learningRate = self.parameters['Learning Rate'][0],\
                momentumRate = self.parameters['Momentum Rate'][0],\
                regression = self.parameters['Regression'][0],\
                adaptiveLearning = self.parameters['Adaptive Learning'][0],\
                adaptiveHistory = self.parameters['Adaptive History'][0],\
                adaptiveAlpha = self.parameters['Adaptive Alpha'][0],\
                adaptiveBeta = self.parameters['Adaptive Beta'][0])
    
class NBayesShim(Shim):
    def __init__(self):
        Shim.__init__(self)

class BaggingShim(Shim):
    def __init__(self):
        Shim.__init__(self)
        self.parameters['Classifier'] = [None, CLASSIFIERSELECTOR,0,0,350]

#types for config
BOOLEAN = 1 # (var, type, default)
INTSELECTOR = 2
FLOATSELECTOR = 3
DROPSELECTOR = 4 # (var, type, list of vals, list of nums)
CLASSIFIERSELECTOR = 5
TEXT = 6
# (var, type, lowerbound, upper)

#types for results
NONE = 0
ENUM = 1
GRAPH = 2
