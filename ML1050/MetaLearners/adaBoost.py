from ML1050.Example import LabeledExample
from ML1050.TrainingSet import TrainingSet
from ML1050.Classifiers import classifier as _classifier
from ML1050 import eps
from random import random as _random
from math import log as _log
from sys import maxint as _MAX_INT

def makeRandomSet(weightedSet):
	"""Returns a new trainingSet by choosing examples based on weight probablitites""" 
	newtrainingSet = []
	
	#Make a list starting with zero and ending with MAX_INT
	#Where all of values inbetween are the probs of choosing this element
	probs = [0]
	for ex in weightedSet:		
		probs.append(ex.weight + probs[-1])
	
	probs.append(_MAX_INT)
		
	for i in range(len(weightedSet)): #Get N new smaples
		randNum = _random()
		for j in range(len(probs) - 1 ):	
			if randNum >= probs[j] and probs[j+1] > randNum : 
				newtrainingSet.append(boostExample(
					LabeledExample(weightedSet[j-1],label=weightedSet[j-1].label) ,weightedSet[j-1].weight) )
				break
		
	
	return newtrainingSet

def sumSet(weightedSet):
	"""Returns the sum of a set of weighted examples"""
	sum = 0
	for example in weightedSet:
		sum += example.weight
	return sum
		
def normalizeProbs(weightedSet):
	"""Normalize the probablites"""
	sum = sumSet(weightedSet)

	for wExample in weightedSet:
		wExample.weight /= sum
	#print "newsum", sumSet(weightedSet)
	return weightedSet

def clacError(classifier,weightedSet):
	"""Return the Error of a learner"""
	error = 0
	for ex in weightedSet:
		if classifier.test(ex) != ex.label:
			error += ex.weight
	return error
	
class boostExample(LabeledExample):
	"""Labeled Examples that have weights"""
	def __init__(self,example, weight):
		
		super(boostExample, self).__init__(example, label = example.label)
		self.weight = weight

	def __repr__(self):
		return "<Ex:%s,W:%s>" % (super(boostExample, self).__repr__(), self.weight)


class boostLearner:
	"""A Classifier that has a B"""
	def __init__(self, inst, B = None):
		self.inst =  inst
		self.B = B	
	def __call__(self):
		return self.inst
		
class adaBoost(_classifier):
	"""Pg 362 of Alpaydin"""
	def __init__(self, listOfClassifiers):
		self.listOfClassifiers = listOfClassifiers
		self.classifiers = [ ]

	def train(self, trainingSet):

		#Init all of the weights to 1/N
		weightedSet = [boostExample(LabeledExample(wExample,label=wExample.label), 1./len(trainingSet)) for wExample in trainingSet] 
		
	
		for thisLearner in self.listOfClassifiers:
			thisLearner.train(weightedSet) #Traning the learner
			error = clacError(thisLearner,weightedSet) 

			#print error
			B = error/(1 - error)
			if error >= 0.5:
				#if error is greater that 0.5 make a new data set and try again
				weightedSet = normalizeProbs(makeRandomSet(weightedSet))
						
			elif B == 0:
				#if prefect classification reset the dataset
				B = eps()
				self.classifiers.append(boostLearner(thisLearner, B))
				weightedSet = [boostExample(LabeledExample(wExample,label=wExample.label), 1./len(trainingSet)) for wExample in trainingSet] 

			else:			
				self.classifiers.append(boostLearner(thisLearner, B))
				#update the weights
				for ex in weightedSet:
					if ex.label == thisLearner.test(ex):
						ex.weight *= B
											
				weightedSet = normalizeProbs(makeRandomSet(weightedSet))


	def test(self, example):
		lables = {}
		#get every classifers prediction
		for learner in self.classifiers:
			choosenLabel = learner.inst.test(example)
			try:
				lables[choosenLabel] += _log(1/learner.B)
			except KeyError:
				lables[choosenLabel] = _log(1/learner.B)

		bestValue = -1 * _MAX_INT 
		bestKey = None
		#find the class with the best
		for key, value in lables.items():
			if value > bestValue:
				bestValue = value
				bestKey = key

		return bestKey

def _test():
	from ML1050.Classifiers.DecisionTree import DecisionTree
	from ML1050.Classifiers.kNN import kNN
	from ML1050.TrainingSet import TrainingSet
	from ML1050 import discreteDistance
	#trainingSet = TrainingSet('/home/dparks/ML/ML1050/Datasets/votes-train0.csv')
	#print trainingSet
	trainingSet = TrainingSet('/home/dparks/ML/ML1050/Datasets/vote.csv')
	learners = []
	for i in range(75):
		learners.append(DecisionTree(0,1))

				
	#learners.append(kNN(10,discreteDistance))
	myBoost = adaBoost(learners)
	myBoost.train(trainingSet)
	print myBoost.validate(trainingSet)
	
if __name__ == "__main__":_test()
