import os
import wx
from pylab import *
from ML1050.TrainingSet import TrainingSet
from ML1050.External.SVM import SVM
from ML1050.TrainingSet import TrainingSet
from ML1050.Example import LabeledExample
from ML1050.Utils.StringMap import StringMapper
from random import random




class Test:
    def __init__(self, numClassifiers=1):
        self.numClassifiers = numClassifiers
        self.parameters = {}
        self.results = {}
        self.resultType = 0
    def run(self,classifiers,trainingSet, classHash):
        #return -1 for fail, 0 for success
        pass
    def setParameter(self, key, value):
        self.parameters[key][0] = value
#(object,type,lowerbound,upperbound, ID)

class MatplotLibExample(Test):
    n_models = 2
    def __init__(self):
        Test.__init__(self, 1)
        #self.parameters['Number of Models']=[self.n_models,INTSELECTOR,1,10,5]
        self.resultType = GRAPH
    def run(self, classifiers, trainingset, classHash):
        
        sm = StringMapper(trainingset)
        ts = [sm.map(t) for t in trainingset]
        trainingset = ts
        classifiers[0].train(trainingset)
        
        bnd = [trainingset[0][0],trainingset[0][0],trainingset[0][1],trainingset[0][1]]
        for e in trainingset:
            if e[0] < bnd[0]:
                bnd[0] = e[0]
            elif e[0] > bnd[1]:
                bnd[1] = e[0]
            if e[1] < bnd[2]:
                bnd[2] = e[1]
            elif e[1] > bnd[3]:
                bnd[3] = e[1]
        if bnd[0] > 0:
            bnd[0] *=0.9
        else:
            bnd[0] *= 1.1
        if bnd[1] < 0:
            bnd[1] *=0.9
        else:
            bnd[1] *= 1.1
        if bnd[2] > 0:
            bnd[2] *=0.9
        else:
            bnd[2] *= 1.1
        if bnd[3] < 0:
            bnd[3] *=0.9
        else:
            bnd[3] *= 1.1
        
        x = arange(bnd[0],bnd[1],0.1)
        y = arange(bnd[2],bnd[3],0.1)
        X,Y = meshgrid(x,y)
            
        clf()
        Z = []
        for i in range(len(X)-1,-1,-1):
            z = []
            for k in range(len(X[0])):
                z.append(self.testpoint(X[i][k], Y[i][k], classifiers[0]))
            Z.append(z)
        im = imshow(Z, extent=(bnd[0],bnd[1],bnd[2],bnd[3]))
        t = ""
        for k in classHash.keys():
            t = t + k + " " + str(classHash[k][0]) + "\n"
        print t
        text(bnd[0]-2,0,t)

        
        d = [{},{}]
        classes = []
        for el in trainingset:
            if not d[0].has_key(el.label):
                d[0][el.label] = []
                classes.append(el.label)
            if not d[1].has_key(el.label):
                d[1][el.label] = []
            d[0][el.label].append(el[0])
            d[1][el.label].append(el[1])
        
        color = ['b.','r.','y.','g.']
        for c in classes:
            plot(d[0][c], d[1][c], color[classes.index(c)])
        axis(bnd)
        savefig("fig.jpg", dpi=100)
        
        
    def testpoint(self,x,y, mod):
        return int(mod.test(LabeledExample([x,y],label=None)))
class KFold(Test):
    nfold=10
    def __init__(self):
        Test.__init__(self, 1)
        self.parameters['Number of Folds']=[self.nfold,INTSELECTOR,1,10,5]
        self.resultType = ENUM
        
    def run(self,classifiers,trainingSet, classHash):
        from ML1050.Preprocessing.CrossValidation import kFold
        from ML1050.Example import LabeledExample
        from ML1050.TrainingSet import TrainingSet
        averageValError = 0.0
        averageTrainError = 0.0
        self.nfold = self.parameters['Number of Folds'][0]
        #print self.nfold
        #we only requested one classifier
       
        for training, validation in kFold(trainingSet, k = self.nfold):
            
            classifiers[0].train(trainingSet)
            validationError = 0.0
            for example in validation:
                try:
                    if classifiers[0].test(example) != example.label: validationError += 1
                except AttributeError:
                    return -1
            validationError = float(validationError)/len(validation)
            averageValError += validationError
            
            trainingError = 0.0
            for example in validation:
                try:
                    if classifiers[0].test(example) != example.label: trainingError += 1
                except AttributeError:
                    return -1
            trainingError = float(trainingError)/len(training)
            averageTrainError += trainingError
        
        dataError = 0.0
        
        for example in trainingSet:
            if classifiers[0].test(example) != example.label: dataError += 1
            
        dataError = float(dataError)/len(trainingSet)
        
        averageValError = averageValError/self.nfold
        averageTrainError = averageTrainError/self.nfold
        
        self.results['Average Validation Set Error'] = averageValError
        self.results['Average Trainging Set Error'] = averageTrainError
        self.results['Whole Data Set Error'] = dataError
        
        return 0

class Tournament(Test):
    def __init__(self):
        Test.__init__(self,2)
        self.resultType = ENUM
    def run(self,classifiers,trainingset, classhash):
        print "got", len(classifiers)
        for i in classifiers:
            print i
        classifiers[0].train(trainingset)
        classifiers[1].train(trainingset)
        
        sumA = 0
        sumB = 0
        for ex in trainingset:
            if classifiers[0].test(ex) == ex.label: sumA += 1
            if classifiers[1].test(ex) == ex.label: sumB += 1
        totalA = float(sumA)/float(len(trainingset))
        totalB = float(sumB)/float(len(trainingset))
        
        self.results['Classifier A got']= totalA
        self.results['Classifier B got']= totalB
        if totalA > totalB: self.results['Result']= "A wins!"
        elif totalB > totalA: self.results['Result']= "B wins!"
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
