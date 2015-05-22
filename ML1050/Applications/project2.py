#!/usr/bin/python
from ML.kNN import kNN
from csv import reader, writer
from random import shuffle 
from string import split
from sys import argv
from ML.preProcess import preProcess
from ML.gaussian import *
from tempfile import mkdtemp
import os.path

##################HELPER FUNCTIONS#############################################################
def csvReader(filename):
	"""read in a csv file"""
	file = open(filename,'r')
	try:
        	inputList = [( row[0], float(row[1]), float(row[2]) ) for row in reader(file)]
	except IndexError:
		inputList = [( row[0], float(row[1]) ) for row in reader(file)]
	file.close()
        return inputList

def csvWriter(filename, inputList ,delim =','):
	"""Write out an inputList to filename, each element in inputList is seperated by delim"""
	file = open(filename,'w')
        myWriter = writer(file, delimiter = delim)
        myWriter.writerows(inputList)
	file.close()

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

def prettyPrint(outputList):
	print "Test\tTraining Acc\tVaildation Acc"
	for row in outputList:
		temp = ""
		for item in row:
			temp += str(item) + "\t"
		print temp


################# KNN TESTS################################################################
def simpleTestK(training, vaildation, k):
	"""Calc training error and validation error by cutting the file in half"""
        mykNN = kNN(k)
       	mykNN.train(training)		    
	return mykNN.validate(training),mykNN.validate(vaildation)
	
def halfAndHalfTestK(inputList , k):
	"""Calc training error and validation error by cutting the file in half"""
        (training,vaildation) = halfIt(inputList)    
	return simpleTestK(training, vaildation, k)
		
def preProccesAndTestK(inputList, k, method, option):
	"""Calc training error and validation error using method and option, 
	where method is a preProccesing method from project1 and option is 
	the arg passed to that method"""

	mySets = preProcess(inputList)
	
	trainingLists, vaildationLists = getattr(mySets,method)(option)

	trainingAccuracys = [ ]
	vaildationAccuracys = [ ]
	
	for i in range(len(trainingLists)):
		trainAcc ,vaildAcc = simpleTestK(trainingLists[i], vaildationLists[i], k)
		trainingAccuracys.append(trainAcc)
		vaildationAccuracys.append(vaildAcc)
	
	return average(trainingAccuracys), average(vaildationAccuracys)


def doABunchOfPreProccesTestKs(inputList, method, option, start, finish, step):
	"""generate a trainingList and vaildationList using project1 code. Then test a range of k vaules and write the results to a 
	appropriately named file"""
	
	outputList = [] #a list holding the results of the test
	
	
	mySets = preProcess(inputList)
	
	trainingLists, vaildationLists = getattr(mySets,method)(option)
	
	for k in range(start,finish+1,step):
	
		trainingAccuracys = [ ]
		vaildationAccuracys = [ ]
		
		for i in range(len(trainingLists)):
			trainAcc ,vaildAcc = simpleTestK(trainingLists[i], vaildationLists[i], k)
			trainingAccuracys.append(trainAcc)
			vaildationAccuracys.append(vaildAcc)
			
		trainError = average(trainingAccuracys)
		vaildError = average(vaildationAccuracys)
		
		print k,trainError,vaildError
		outputList.append((k,trainError,vaildError))
	
	
	return outputList
	
#################GAUSSIAN TESTS################################################################################	
def simpleTestGauss(training, vaildation, gaussFunction):
	"""Takes a trainingList, a vaildationList and a method of computing discrimate functions, and returns traing and vaildation error"""
	mygauss = gaussian()
	mygauss.train(training, method)
	return (mygauss.validate(training), mygauss.validate(vaildation))

def halfAndHalfTestGauss(inputList , gaussFunction):
	"""Calc training error and validation error by cutting the file in half use Gauss classifier"""
        (training,vaildation) = halfIt(inputList)
		    
	return simpleTestGauss(training,vaildation,method)
	
def preProccesAndTestGuass(inputList, gaussFunction, preProcessFunction, option):
	mySets = preProcess(inputList)
	
	trainingLists, vaildationLists = getattr(mySets,preProcessFunction)(option)

	trainingAccuracys = [ ]
	vaildationAccuracys = [ ]
	
	for i in range(len(trainingLists)):
		trainingAcc, vaildationAcc =  simpleTestGauss(trainingLists[i], vaildationLists[i], gaussFunction)			
		trainingAccuracys.append(trainingAcc)
		vaildationAccuracys.append(vaildationAcc)
	
	
	return average(trainingAccuracys), average(vaildationAccuracys)

def preProcessAndTestAllGaussFunctions(inputList, preProcessFunction, option):
	mySets = preProcess(inputList)
	trainingLists, vaildationLists = getattr(mySets, preProcessFunction)(option)
	
	listOfGaussFuctions = [differentHyperEllipsoidal,
				sharedHyperEllipsoidal,
				sharedAxisAligned,
				sharedHyperSpheric,
				naiveBayes,
				eq528 ]
	outputList = [] 
	for gaussFunction in listOfGaussFuctions:
		trainingAccuracys = [ ]
		vaildationAccuracys = [ ]
		
		for i in range(len(trainingLists)):
			trainingAcc, vaildationAcc =  simpleTestGauss(trainingLists[i], vaildationLists[i], gaussFunction)			
			trainingAccuracys.append(trainingAcc)
			vaildationAccuracys.append(vaildationAcc)
	
		outputList.append((gaussFunction.__name__,average(trainingAccuracys),average(vaildationAccuracys)))
	return outputList

	

#print halfAndHalfTestK(csvReader("data/haykin.csv") , 1)
#print preProccesAndTestK(csvReader("data/haykin.csv"), 50, "kFold", 3 )
#prettyPrint(doABunchOfPreProccesTestKs(csvReader("data/haykin.csv"), "kFold", 3, 50, 60, 1))

#print halfAndHalfTestGauss(csvReader("data/haykin.csv"), differentHyperEllipsoidal )	
#print preProccesAndTestGuass(csvReader("data/haykin.csv"), differentHyperEllipsoidal, "kFold", 10)
#prettyPrint(preProcessAndTestAllGaussFunctions(csvReader("data/haykin.csv"),"kFold", 10))

#print halfAndHalfTestGauss(csvReader("data/singleGauss.csv"), singleGaussian )



