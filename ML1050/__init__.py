from math import log as _log, sqrt as _sqrt

missingValueSymbol = '?'

def squaredDistance(point1, point2):
	"""Find the distance between two points in any dimention. Note this 
	is only a discriminate function and doesn't compute the actual 
	distance"""
			
	sumOfDistances = 0

	for i in range(len(point1)):
		sumOfDistances += (point1[i] - point2[i]) ** 2
	return sumOfDistances
	
def euclideanDistance(point1, point2):
	return _sqrt(squaredDistance(point1, point2))
	
def manhattanDistance(point1,point2):
	sumOfDistances = 0

	for i in range(len(point1)):
		sumOfDistances += abs(point1[i] - point2[i]) 
	return sumOfDistances
	
def discreteDistance(point1,point2):
	"""Distance of two discrete attributes"""
	sumOfDistances = 0
	for i in range(len(point1)):
		if point1[i] != point2[i]:
			sumOfDistances +=1
			
	return sumOfDistances
	
def log2(x):
	""" Compute the log (base 2) of a number."""
	#python log is ln so div by the log of 2 get a base change
	#0.69314718055994529 == _log(2)
	return _log(x)/(0.69314718055994529)
	
def halfIt(inputList):
	"""cut a list in half"""
        cut = len(inputList)/2
        return (inputList[:cut],inputList[cut:])

def average(mylist):
	"""Calc the average of a list"""
	sum = 0
	for item in mylist:
		sum += item
	return float(sum)/len(mylist)
	
class __eps:
	"""Returns machine eps""" 
	def __init__(self):
		self.__eps = None
	def __call__(self):
		if not self.__eps:
			self.__eps = 1
			while (self.__eps/2. + 1.) > 1.:
				self.__eps = self.__eps / 2.
				
		return self.__eps
		
eps = __eps()		
		
def sortBy(list, n):
	"""Sort a list by atrribute n, credit: BDFL"""
	nlist = map(lambda x, n=n: (x[n], x), list)
	nlist.sort()
	return map(lambda (key, x): x, nlist)
