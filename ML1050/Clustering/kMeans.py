from ML1050.Example import LabeledExample
from ML1050.TrainingSet import createTrainingSet
from ML1050 import squaredDistance as _squaredDistance
from ML1050 import manhattanDistance as _manhattanDistance
from random import randint as _randint
from sys import maxint as _MAX_INT

def makeNoneList(size):
	result = []
	for i in range(size):
			result.append(None)
	return result
	
class clusteredExample:
	def __init__(example, cluster):
		self.example = example
		self.cluster = cluster
	
	def __repr__(self):
		return "<Ex:%s, Cluster:%s>" % (self.example.__repr__, self.cluster)
			
	def __call__(self):
		return self.cluster

class kMeans:
	def __init__(self, distanceFunction, k = 3, maxIterations = 1000, threshold = 0.00001):
		self.k = k
		self.maxIterations = maxIterations
		self.threshold = threshold
		self.means = makeNoneList(self.k)
		self.dist = distanceFunction

	def findCluster(self, label):
		for key,value in self.clusters.items():

			for item in value:
				if item.label == label:
					print value
					return key

		
	def train(self, trainingSet):
		if self.k > len(trainingSet):
			raise NotImplementedError( ' Too Many Clusters')
		currentIteration = 0
		meanChange = _MAX_INT
		#newMeans = makeNoneList(self.k)
		
		while (currentIteration < self.maxIterations) and ( meanChange > self.threshold):
			clusteredExamples = self.__reCluster(trainingSet)
			newMeans = self.__reClacMeans(clusteredExamples)
			meanChange = self.__meanChange(newMeans)
			#print meanChange	
			self.means = newMeans
			currentIteration +=1
		
		self.clusters = clusteredExamples
		
	def __reCluster(self,trainingSet):
		#Choose k random means from the trainingSet
		for i in range(self.k):
			if self.means[i] == None:
				self.means[i] = (trainingSet[ _randint(0,len(trainingSet) - 1 ) ] )
		
		clusteredExamples = {}
		#for every example int the training set figure out which cluster is belongs to
		for example in trainingSet:
			newCluster = self.__findCluster(example)
			try:
				clusteredExamples[newCluster].append(example)
			except KeyError:
				clusteredExamples[newCluster] = [ example ]
				
		return clusteredExamples
		
	def __findCluster(self, example):
		smallestDist = _MAX_INT
		bestCluster = None
		for i in range(self.k):
			thisDist = self.dist(self.means[i], example)
			if thisDist < smallestDist:
				smallestDist = thisDist
				bestCluster = i
				
		return bestCluster
		
	def __reClacMeans(self, clusteredExamples):
		newMeans = [ ]
		
		for i in range(self.k):
			try:
				listOfExamples = clusteredExamples[i]
				newList = list(listOfExamples[0])
				sum = LabeledExample(newList, label = "Mean")

				
				for thisExample in listOfExamples[1:]:
					for i in range(len(thisExample)):
						sum[i] += thisExample[i]
						
				for i in range(len(sum)):
					sum[i] /= float(len(listOfExamples))
				newMeans.append(sum)
				
			except KeyError:
				newMeans.append(None) 
		return newMeans

	def __meanChange(self, newMeans):
		sum = 0
		for i in range(self.k):
		
			if self.means[i] == None or newMeans[i] == None:
				return _MAX_INT
			else:
				sum += _manhattanDistance(newMeans[i],self.means[i])
		return sum
			
	def __repr__(self):
		return self.clusters.__repr__()

	def test(self, example):
		return self.__findCluster(example)
		
def _test():
	trainingSet = createTrainingSet([
LabeledExample(['A', 1, 2, 3, 4]),
LabeledExample(['B', 1, 2, 3, 4]),
LabeledExample(['C', 0, 0, 0, 0]),
LabeledExample(['D', 3, 3, 3, 3]),
LabeledExample(['E', 3, 3, 3, 4]),
LabeledExample(['F', 1, 1, 1,1])
])

	myKMeans = kMeans(_squaredDistance)
	myKMeans.train(trainingSet)
	print myKMeans
if __name__ == "__main__":_test()
