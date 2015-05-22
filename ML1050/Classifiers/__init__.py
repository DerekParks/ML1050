"""This provides the abstract classifier class that all other classifiers will inherit"""
def _abstract():
	import inspect
	caller = inspect.getouterframes(inspect.currentframe())[1][3]
	raise NotImplementedError(caller + ' must be implemented in subclass')

class classifier:
	"""Abstract Classifier Class"""
	def train(self, trainingList):
		"""Should take a sequence, where the first item is the class and the rest of the items are the input values to get the given class"""
		_abstract()
	def test(self, sample): 
		"""Give a sample input and return the predicted class"""
		_abstract()

	def validate(self, inputList):
		"""Takes a List where first element is class and the rest are the inputs, returns Error"""
		wrongCount = 0
		for row in inputList:
			temp = self.test(row)
			#print temp, row.label
			if temp != row.label:
				wrongCount += 1
			

		#print wrongCount
		#print len(inputList)
		return (float(wrongCount)/len(inputList))
		
def _test():
	mylist = [] 
	myClassifier = classifier()
	myClassifier.train(mylist)
	

if __name__ == "__main__": _test()
