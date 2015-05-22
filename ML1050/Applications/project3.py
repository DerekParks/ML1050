#!/usr/bin/python
#Derek Parks
#Project 3
#4 - 21 - 05
#see bottom of code or example of how to call functions!!!

from ML1050.Classifiers.DecisionTree import DecisionTree
from ML1050.TrainingSet import TrainingSet
from ML1050.Preprocessing.CrossValidation import kFold
from ML1050 import average
from ML1050.MetaLearners.adaBoost import adaBoost
from sys import maxint as _MAX_INT

def justOne(filename, thres):
	"""Run a DecisionsTree on a and file print errors""" 
	trainingSet = TrainingSet(filename)
	
	trainingAccs = []
	validAccs = []
	for training,validation in kFold(trainingSet):		
		myDTree = DecisionTree(threshold=thres)
		myDTree.train(training)
		trainingAccs.append(myDTree.validate(training))
		validAccs.append(myDTree.validate(validation))
		
	print "Validation:",average(validAccs), "Training:",average(trainingAccs), "WholeDataSet:",myDTree.validate(trainingSet)	
	
def iterateOverThres(filename):
	"""Iterate over a bunch of thresholds an return the best"""
	trainingSet = TrainingSet(filename)
		
	bestThres = None
	bestAcc = _MAX_INT
	for i in range(0,40):
		j = i/100.0 + .1
		trainingAccs = []
		validAccs = []
	
		for training,validation in kFold(trainingSet):		
			myDTree = DecisionTree(threshold=j)
			myDTree.train(training)
			trainingAccs.append(myDTree.validate(training))
			validAccs.append(myDTree.validate(validation))
		
		accs = 	average(validAccs)
		if accs <= bestAcc:
			bestAcc = accs
			bestThres = j
			
		print j,accs, average(trainingAccs), myDTree.validate(trainingSet)
	return bestThres

def boostIt(filename, numLearners, treeHeight):	
	trainingSet = TrainingSet(filename)
	for training,validation in kFold(trainingSet):
		
		trainingAccs = []
		validAccs = []
		learners = []
		for i in range(numLearners):
			learners.append(DecisionTree(0,treeHeight))

	
		myBoost = adaBoost(learners)
		myBoost.train(training)
		trainingAccs.append(myBoost.validate(training))
		validAccs.append(myBoost.validate(validation))
	
	print "Validation:",average(validAccs), "Training:",average(trainingAccs), "WholeDataSet:",myBoost.validate(trainingSet)
	

#Note all classifiers run with 10 Fold Cross Validation
#Run Mike's vote data set
#justOne('/home/dparks/ML/ML1050/Datasets/votes-train0.csv',0.233)

#Run the mushroom data set
#justOne('/home/dparks/ML/ML1050/Datasets/mushroom.csv',0.17)

#Run the orginal vote data set
#justOne('/home/dparks/ML/ML1050/Datasets/vote.csv',0.45)

#Run adaBoost Mike's Vote Dataset

#boostIt('/home/dparks/ML/ML1050/Datasets/votes-train0.csv', i + 30, 1)

#print iterateOverThres('/home/dparks/ML/ML1050/Datasets/votes-train0.csv')
#print iterateOverThres('/home/dparks/ML/ML1050/Datasets/mushroom.csv')
#print iterateOverThres('/home/dparks/ML/ML1050/Datasets/vote.csv')

