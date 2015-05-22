


from TrainingSet import TrainingSet
from TrainingSet import createTrainingSet
from Example import LabeledExample
import math

def standardize(inputData):
	"""The classification of some numerical data sets may be
	improved by standardizing the data.  This method shifts
	the data, so that the mean is zero, and scales it so the
	standard deviation is one.  standardize returns a 
	TrainingSet that is a scaled copy of the input
	TrainingSet.
	
	In the example below, the input data set is sliced for
	simplification. "print str(output).replace('>,','>,\n')" is 
	used to display the output in a more readable format.
	
	>>> from TrainingSet import TrainingSet
	>>> from Preprocessing.StandardizeData import standardize
	>>> input = TrainingSet('Datasets/NBA_TRAIN.csv')
	>>> output = standardize(input)
	>>> print output[0].label
	2
	>>> print "%.5f" % (output[0][0])
	0.77118
	>>> print "%.5f" % (output[0][1])
	0.26551
	
	
	"""
	mean = []
	std_dev = []
	
	for i in range(len(inputData[0])):
		mean.append(0.0)
		std_dev.append(0.0)
	
	#exampleList = []
	
	#newExampleList = [originalExample.label]
	
	#calculate means
	for example in inputData:
		for i in range(len(example)):
			mean[i] = mean[i] + example[i]
	for i in range(len(mean)):
		mean[i] = mean[i] / len(inputData)
	
	#calculate standard deviations
	for example in inputData:
		for i in range(len(example)):
			std_dev[i] = std_dev[i] + (example[i] - mean[i])**2
	for i in range(len(std_dev)):
		std_dev[i] = math.sqrt(std_dev[i] / len(inputData))
		
	newExampleList = []
	for example in inputData:
		newExample = [example.label]
		for i in range(len(example)):
			if std_dev[i] != 0.0:
				newExample.append((example[i] - mean[i]) / std_dev[i])
			else:
				newExample.append(example[i] - mean[i])

		newExampleList.append(LabeledExample(newExample))
		
	return createTrainingSet(newExampleList, False)
	
	
		
	""""
		#caluclate standard deviation
		for datum in range(len(originalExample)):
			std_dev = std_dev + (datum - mean)**2
		std_dev = math.sqrt(float(std_dev) / len(originalExample))
		
		#shift data so mean is zero and scale so data to a standard deviation of one
		for datum in originalExample:
			datum = (datum - mean)
			if std_dev != 0.0:
				datum = datum / std_dev
			newExampleList.append(datum)
			
		exampleList.append(LabeledExample(newExampleList))
		
		
	#autoConvert needs to be set to False, Why?, ask Mike.
	return createTrainingSet(exampleList, False)
	"""	
			
def _test():
	"""Run the tests in the documentation strings."""
	import doctest
	return doctest.testmod(verbose=True)

if __name__ == "__main__":
	try:
		__IP                            # Are we running IPython?
	except NameError:
		_test()                         # If not, run the tests
		