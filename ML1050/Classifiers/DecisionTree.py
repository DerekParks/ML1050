
from math import log as _log
from ML1050.Example import LabeledExample
from ML1050.TrainingSet import createTrainingSet
from ML1050.Classifiers import classifier as _classifier
from ML1050 import log2 as _log2,missingValueSymbol, sortBy as _sortBy
from random import random as _random
from sys import maxint as _MAX_INT



class DecisionTree(_classifier):

	def __init__(self, threshold=0.00001, maxHeight = 50):
		self.threshold = threshold
		self.maxHeight = maxHeight
		_DecisionNode.threshold = threshold
		_DecisionNode.maxHeight = maxHeight

		self.rootNode = None
		
	def train(self, trainingSet):	
		_DecisionNode.majorityClass = _getMajority(trainingSet, trainingSet[0].label)
		#print _DecisionNode.majorityClass
		
		self.rootNode = _DecisionNode("Root","Root","Root",0, len(trainingSet))
		self.rootNode.makeChildren(trainingSet)
		#print self.rootNode
		
	def __repr__(self):
		return self.rootNode.__repr__()
	
	def test(self, example):
		return self.rootNode.test(example)
		
	def __call__(self, example):
		"""
		Calling an instance like a function is used to test a new example. 
		"""
		return self.test(example)

		
class _DecisionNode:
	threshold = None
	maxHeight = None
	majorityClass = None
	
	def __init__(self, atrributeIndex, attributeLabel, nodeType, height, length, value = None):
		self.atrributeIndex = atrributeIndex
		self.attributeLabel = attributeLabel
		self.nodeType = nodeType
		self.height = height
		self.children = [ ]
		self.length = length
		self.value = value
		
	def __call__(self, example):
		return self.test(example)

	def __repr__(self):
		"""Print yourself then your children"""
		outputStr = ""
		for i in range(self.height):
			outputStr += "\t"
		outputStr += "Type=%s, Label=%s Index=%s Value=%s\n" % (self.nodeType,self.attributeLabel,self.atrributeIndex, self.value)
		for child in self.children:
			outputStr += child.__repr__()
		return outputStr
		
	def getLargestChild(self):
		"""Returns the child with the most atrributes following it"""
		bestChild = None
		largest = -1
		for child in self.children:
			if child.length > largest:
				 bestChild= child
				 largest = child.length
				 
		return bestChild
		
	def getLargestChildNew(self):
		"""Randomly Choose a child based on size"""
		sum = 0	
		for child in self.children:
			sum += child.length
		
		randNum = _random()
		previous = 0
		prob = 0
		for child in self.children:
			prob += child.length/float(sum)
			if randNum >= previous and prob > randNum :
				return child			
			previous = prob		
		return self.children[-1]
		
	def test(self,example):
		if self.nodeType == "Node":
			if self.value == None: #Discerete Node
				if example[self.atrributeIndex] == self.attributeLabel:
					return self.testAllChildren(example)
				else:
					return False
					
			else: #Numeric Node
				if self.attributeLabel == "<=": #less than equal to  node
					if example[self.atrributeIndex] <= self.value:
						return self.testAllChildren(example)
					else:
						return False
				else:#greater than node
					if example[self.atrributeIndex] > self.value:
						return self.testAllChildren(example)
					else:
						return False
						
		elif self.nodeType == "Leaf":
			return self.attributeLabel
			
		elif self.nodeType == "Root":
			#print self.testAllChildren(example)
			return self.testAllChildren(example)
				
	def testAllChildren(self,example):
		"""Test all of your children to see which path the example should go down"""
		for child in self.children:
			returnValue = child.test(example)
			if returnValue != False:
				return returnValue
		
		#if you get to here all the children have returned false
		#choose a child
		child = self.getLargestChildNew()
		example[child.atrributeIndex] = child.attributeLabel
		return child.test(example)	
						
	def makeChildren(self,trainingSet):
		"""Build all of your children"""

		e = _entropy(trainingSet)
		
		#test for stopping conditions
		if (e < self.__class__.threshold) or (self.height > self.__class__.maxHeight) or (e == 1.0 and self.nodeType == "Node"):
			self.children.append(_DecisionNode("Equal", 
				_getMajority(trainingSet, self.__class__.majorityClass), 
				"Leaf", 
				self.height + 1, 
				len(trainingSet)))
		

		else: #make all your children
			bestAtrributeIndex, bestValue = _getAtrribute(trainingSet)
			splitOnBestAtrribute = _splitByIndex(trainingSet, bestAtrributeIndex, bestValue)
			
			for attributeLabel, splitTrainingSet in splitOnBestAtrribute.items():
				nextChild = _DecisionNode(bestAtrributeIndex, 
					attributeLabel, 
					"Node", 
					self.height + 1,
					len(splitTrainingSet),
					bestValue)
					
				nextChild.makeChildren(splitTrainingSet)
				self.children.append(nextChild)
				

				
def _informationGain(trainingSet, attributeIndex, splitValue = None):
	"""Compute the information gain of spliting on a giving attribute"""
	entroyBefore = _entropy(trainingSet)
	splits = _splitByIndex(trainingSet, attributeIndex, splitValue)
	sum = 0;
	for label, splitTraningSet in splits.items():
		sum += (len(splitTraningSet)/float(len(trainingSet))) * _entropy(splitTraningSet)
		return entroyBefore - sum 	

	


def _getAtrribute(trainingSet):
	""" Returns the best atrributeIndex to split on"""
	numberAttributes = len(trainingSet[0]) #assume all examples are of same length	
	bestGain = -1
	bestAttribute = None
	bestValue = None
	
	for attributeIndex in range(numberAttributes):
		
		#Make sure don't have missingValueSymbol determing type
		i = 0
		while trainingSet[i][attributeIndex] == missingValueSymbol:
			i += 1
		
		thisAttributesType = type(trainingSet[i][attributeIndex]) #assume all atrributes have this type
		
		if thisAttributesType == type("String"): #Discrete atrribute
			gain = _informationGain(trainingSet, attributeIndex)
			if gain >= bestGain:
				bestGain = gain
				bestAttribute = attributeIndex
		
		elif thisAttributesType == type(0.0) or thisAttributesType == type(0):

			trainingSet = _sortBy(trainingSet, attributeIndex)
			
			for j in range(1,len(trainingSet)): #Numeric atrribute
			
				if trainingSet[j-1].label != trainingSet[j].label:
					gain = _informationGain(trainingSet, attributeIndex, trainingSet[j-1][attributeIndex])

					if gain >= bestGain:
						bestGain = gain
						bestAttribute = attributeIndex
						bestValue = trainingSet[j-1][attributeIndex]
			
			#if bestVale == None:
				
			
	return 	bestAttribute, bestValue
	

	

def _splitByIndex(trainingSet, attributeIndex, splitValue):
	"""Splits traningSet based on attributeIndex and splitvalue"""
	if splitValue == None:
		return _splitByIndexDiscrete(trainingSet, attributeIndex)
	else:
		return _splitByIndexNumeric(trainingSet, attributeIndex, splitValue)
		

def _splitByIndexNumeric(trainingSet, attributeIndex, splitValue):
	"""Splits traningSet based on attributeIndex and splitvalue"""
	
	
	splitByIndex = {"<=":[], ">":[]}
	for example in trainingSet:
	
		#if there is a missing atrrbiute skip it, Might do something smarter later
		if example[attributeIndex] == missingValueSymbol:
			continue
			
		
		if example[attributeIndex] <= splitValue:
			splitByIndex["<="].append(example)
		else:
			splitByIndex[">"].append(example)
		
	return splitByIndex

def _splitByIndexDiscrete(trainingSet, attributeIndex):
	"""Splits traningSet based on attributeIndex"""
	
	
	splitByClass = {}
	for example in trainingSet:
		#print attributeIndex
		#print example[attributeIndex]
		try:
			splitByClass[example[attributeIndex]].append(example)
		except KeyError:
			splitByClass[example[attributeIndex]] = createTrainingSet([])
			splitByClass[example[attributeIndex]].append(example)
		
	return splitByClass

def _splitByIndexDiscreteWithMissing(trainingSet, attributeIndex):
	"""Split each class based on attributeIndex if an atrribute is missing group with majority"""
	
	splitByClass = {}
	for example in trainingSet:
		try:
			splitByClass[example[attributeIndex]].append(example)
		except KeyError:
			splitByClass[example[attributeIndex]] = createTrainingSet([])
			splitByClass[example[attributeIndex]].append(example)
		

	#Check to see if there are any missing atrributes
	if splitByClass.has_key(missingValueSymbol) and len(splitByClass) != 1:
		
		biggestLen = -1
		biggestClass = None
		
		#find the majority class
		for split,values in splitByClass.items():
			if split == missingValueSymbol:
				continue
			elif len(values) > biggestLen:
				biggestLen = len(values)
				biggestClass = split
			
		#add missing attr class to majority and del it
		splitByClass[biggestClass].extend(splitByClass[missingValueSymbol])
		del(splitByClass[missingValueSymbol])
		
	return splitByClass
		
def _getMajority(trainingSet, tieBreaker):
	"""return the majority class of a trainingSet"""
	counts = _countsByClass(trainingSet)
	
	maxValue = 0
	best = None
	tie = False
	for key,value in counts.items():
		if value > maxValue: 
			tie = False
			best = key
			maxValue = value
		elif value == maxValue:			
			tie = True

	if tie:
		return tieBreaker
	else:
		return best
		

def _countsByClass(trainingSet):
	"""Count the number of instances of each class"""
	countByClass = {}
	for example in trainingSet:
		try:
			countByClass[example.label] += 1
		except KeyError:
			countByClass[example.label] = 1

		
	return countByClass
	

def _entropy(trainingSet):
	"""Compute the entropy of a set of examples."""
	
	countOfLabels = _countsByClass(trainingSet)

	entropy = 0
	for count in countOfLabels.values():
		p = float(count)/len(trainingSet)
		entropy -=  p * _log2(p)

	return entropy



def aFunc():
	"""A test function """
	trainingSet = createTrainingSet([
	LabeledExample(["Y", 'Sunny',1]),
	LabeledExample(["N", 'Sunny',2]),
	LabeledExample(["N", 'Sunny',1]),
	LabeledExample(["Y", 'Sunny',2])
	])

	
	#print _getAtrribute(trainingSet)
	#print splitAtrribute(trainingSet)
	myDTree =DecisionTree(maxHeight=5)
	myDTree.train(trainingSet)
	print myDTree
	#print myDTree(LabeledExample(['None', 'd', 'Hot', 'Normal','Weak']))
	print myDTree.test(LabeledExample(["Y", 'Sunny',2]))
	print myDTree.test(LabeledExample(["N", 'Sunny',1]))
	
	print myDTree.validate(trainingSet)

		
    
if __name__ == "__main__":
	aFunc()
	


"""LabeledExample(['Yes', 'Overcast', 'Hot', 'High','Weak']),
LabeledExample(['Yes', 'Rain', 'Mild', 'High','Weak']),
LabeledExample(['Yes', 'Rain', 'Cool', 'Normal','Weak']),
LabeledExample(['No', 'Rain', 'Cool', 'Normal','Strong']),
LabeledExample(['Yes', 'Overcast', 'Cool', 'Normal','Strong']),
LabeledExample(['No', 'Sunny', 'Mild', 'High','Weak']),
LabeledExample(['Yes', 'Sunny', 'Cool', 'Normal','Weak']),
LabeledExample(['Yes', 'Rain', 'Mild', 'Normal','Weak']),
LabeledExample(['Yes', 'Sunny', 'Mild', 'Normal','Strong']),"""
