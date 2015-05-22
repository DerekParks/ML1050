from ML1050.Example import LabeledExample
from ML1050.TrainingSet import TrainingSet
from ML1050.TrainingSet import createTrainingSet
from scipy import array
from ML1050.Preprocessing.FisherLinearDiscriminant import *
from scipy import array
from pylab import *
#data = TrainingSet('../Datasets/LinearlySeparableNormal.csv')
data = TrainingSet('../Datasets/newDataset.csv')
#data = TrainingSet('../Datasets/bishop_synthetic.csv')
print "d = 1"
fisher = FisherLinearDiscriminant(data, d=1)
print "W:"
print fisher.W
blue = []
bluey = []
red = []
redy= []
for dataItem in data:
  if dataItem.label=='0':
    blue.append(fisher.project(dataItem)[0][:])
    bluey.append(0)
  elif dataItem.label=='1':
    red.append(fisher.project(dataItem)[0][:])
    redy.append(0)

plot(blue,bluey,'bo')
plot(red,redy,'r.')
show()
