#! /usr/bin/python
from ML1050.Classifiers.kNN import kNN

from ML1050.Example import LabeledExample
from ML1050.TrainingSet import createTrainingSet
from ML1050.TrainingSet import TrainingSet
example1 = LabeledExample(['y', 'a', 'a', 'a'])
example2 = LabeledExample(['n', 'b', 'b', 'b'])
trainingSet = createTrainingSet([example1, example2])
testExample = LabeledExample([None, 'a', 'a', 'b'])
def d(ex1, ex2):
    dist = len(ex1)
    for i in range(len(ex1)):
		if ex1[i] == ex2[i]:
			dist -= 1
    return dist

k = kNN(1, d)
trainingSet = TrainingSet('../Datasets/NBA_TRAIN.csv')
k.train(trainingSet)
k.test(testExample)

