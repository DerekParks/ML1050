#!/usr/bin/python
from random import uniform as _uniform, shuffle as _shuffle
from math import exp as _exp, log as _log
from sys import maxint as _MAXINT


def _sigmoid(x):
	if x < -50:
		return 0.
	elif x > 20:
		return 1.
	else:
		return 1./(1.+_exp(-1*x))

def _mulVectors(X1,X2):
	sum = 0;
	for i in range(len(X1)):
		sum += X1[i] * X2[i]
	
		if sum > 1e250:
			return 0
		#print "i:%i,X1:%d,X2:%d" % (i, X1[i],X2[i])
	#print "Sum",sum 
	return sum
	
def _subVectors(X1,X2):
	result = []
	for i in range(len(X1)):
		result.append(X1[i] - X2[i])
		
	return result
def _addVectors(X1,X2):
	result = []
	for i in range(len(X1)):
		result.append(X1[i] + X2[i])
		
	return result
	
def _constTimesVectors(C,X2):
	result = []
	for i in range(len(X2)):
		result.append(C * X2[i])
		
	return result

def _myLog(x):
	if x == 0:
		return 0
	else:
		return _log(x)
		
def _absSumMatrix(alist):
	sum = 0
	for item in alist:

		for el in item:
			
			sum += _sigmoid(abs(el)) - .5
	
	return sum/float(len(alist) * len(item))
	
def _myExp(x):
	if x < 0.00000001:
		return 0
	elif x > 500:
		return 1e200
	else:
		return _exp(x)		
		
def _getClassFromLabel(alist):
	classLabel = 1
	for x in alist:
		if x == 1:
			return classLabel
		else:
			classLabel += 1	

class NeuralNetwork:

	def __init__(self, inputs, outputs, hiddenUnits, learningRate, momentumRate):
		self.H = hiddenUnits
		self.K = outputs
		self.D = inputs + 1
		self.lRate = learningRate
		self.mRate = momentumRate
		
		self.V = []
		self.W = []


		#Init W to small random numbers
		for h in range(self.H):
			nextRow = []
			for j in range(self.D):
				 nextRow.append(_uniform(-1,1))
			self.W.append(nextRow)
			
		#Init V to small random numbers
		for i in range(self.K):
			nextRow = []
			for h in range(self.H):
				nextRow.append(_uniform(-1,1))
			self.V.append(nextRow)
			
		
		self.lastDeltaW = []
		for h in range(self.H):
			self.lastDeltaW.append([0 for j in range(self.D)])

				
	def _initY(self):
		Y = []
		for i in range(self.K):
			Y.append(0)
		return Y
	
	def _initZ(self):
		Z = [1]
		for h in range(1,self.H): #Don't do the first
			Z.append(0)
		return Z
	def _transformEx(self,example):
		x = [1]
		x.extend(example)			
		r = example.label
		return x,r
	
	def train(self, trainingSet):	
		_shuffle(trainingSet)
		sumDeltaW = 0
		sumDeltaV = 0
		for example in trainingSet:
			x,r = self._transformEx(example)			
			
			Y = self._initY()
			Z = self._initZ()
			
			for h in range(1,self.H):
				Z[h] = _sigmoid(_mulVectors(self.W[h],x))
				#print Z[h]
			
			for i in range(0,self.K):
				Y[i] = _mulVectors(self.V[i],Z)
				
			deltaV = []	
			for i in range(self.K):
				deltaV.append(_constTimesVectors(self.lRate * (r[i] - Y[i]) , Z))
				
			deltaW = []
			
			for h in range(self.H):
				sumError = 0
				for i in range(self.K):
					sumError += (r[i] - Y[i]) * self.V[i][h]

				wh = _constTimesVectors(self.lRate * sumError * Z[h] * (1 - Z[h]), x)
				#now calc mommentum
				momentum = _constTimesVectors(self.mRate,self.lastDeltaW[h])
				deltaW.append(_addVectors(wh,momentum))
				
				
			self.lastDeltaW = deltaW

				
			for i in range(self.K):
				self.V[i] = _addVectors(self.V[i], deltaV[i])
				if self.V[i] == float('nan'):
					self.V[i] = 0
			for h in range(self.H):
				self.W[h] = _addVectors(self.W[h], deltaW[h])
				if self.W[h] == float('nan'):
					self.W[h] = 0
								
			sumDeltaW += _absSumMatrix(deltaW)
			sumDeltaV += _absSumMatrix(deltaV)
			
		return sumDeltaW/len(trainingSet), sumDeltaV/len(trainingSet)
			
	def __repr__(self):
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
		
	def testRegression(self, example):
		x = [1]
		x.extend(example)

		Y = self._initY()
		Z = self._initZ()
		
		for h in range(1,self.H):	
			Z[h] = _sigmoid(_mulVectors(self.W[h],x))

		for i in range(0,self.K):
			Y[i] = _mulVectors(self.V[i],Z)
		
		return Y
	
	def testClassification(self, example):
		"""for classification"""
		Y = self.testRegression(example)
		
		#do softmax function
		sum = 0
		for y in Y:
			sum += _myExp(y)
			
		result = []
		for y in Y:
			result.append(_myExp(y)/sum)
			
		return result
	
	def validateClassification(self, trainingSet):
		wrongCount = 0

		
		for example in	trainingSet:
			
			chossenClass = None
			bestOutput = -1 * _MAXINT
			
			for output in example:
				classPos = 1
				if output >= bestOutput:
					output = bestOutput
					chossenClass = classPos
				else:
					classPos += 1
			
			if chossenClass != _getClassFromLabel(example.label):
				wrongCount += 1
				
		return float(wrongCount)/len(trainingSet)
		
	def validateRegression(self, trainingSet):
		sums = [0 for x in range(self.K)]
		
		for example in trainingSet:
			Y = self.testRegression(example)
			#print example, Y
			
			for i in range(0,self.K):
				sums[i] += abs(Y[i] - example.label[i])
						
		return [x/float(len(trainingSet)) for x in sums]
	
	def __call__(self, example):
		"""
		Calling an instance like a function is used to test a new example. 
		"""
		return self.test(example)

def test():
	from ML1050.TrainingSet import createTrainingSet
	from ML1050.TrainingSet import TrainingSet
	from ML1050.Example import LabeledExample


	myNN = NeuralNetwork(inputs = 2, outputs = 1, hiddenUnits = 4, learningRate = .7, momentumRate = .3)

	trainingSet = TrainingSet()
	trainingSet.append(LabeledExample([1,1], label = [0]))
	trainingSet.append(LabeledExample([1,0], label = [1]))
	trainingSet.append(LabeledExample([0,1], label = [1]))
	trainingSet.append(LabeledExample([0,0], label = [0]))
	
	print trainingSet
	for i in range(500):
		#print "Epoc",i 
		print myNN.train(trainingSet)


	print myNN	
	print trainingSet[0].label,myNN.testRegression(trainingSet[0])
	print trainingSet[1].label,myNN.testRegression(trainingSet[1])
	print trainingSet[2].label,myNN.testRegression(trainingSet[2])
	print trainingSet[3].label,myNN.testRegression(trainingSet[3])
	print myNN.validateRegression(trainingSet)
	
if __name__ == "__main__":
	test()
