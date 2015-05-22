from pylab import *
from ML1050.TrainingSet import TrainingSet
from ML1050.Example import LabeledExample
from ML1050.Classifiers.AdaBoost import AdaBoost
from ML1050.Classifiers.DecisionTree import DecisionTree
from math import *

def testpoint(x,y, mod):
    #print x,y
    return int(mod.test(LabeledExample([x,y],label=None)))

ts = TrainingSet('../Datasets/bishop_synthetic.csv')
d = DecisionTree(maxDepth = 1)
m = []
n_models = 3
count = 0
no_c = 0 # count the number it gets correct to evaluate the model parameters
for i in range(n_models):
    no = (i+1)*3
    m.append(AdaBoost(d, M = no))
    m[count].train(ts,useSamples=True)

    for s in ts:
        point = testpoint(s[0], s[1], m[count])
        if int(point) == int(s.label):
            no_c += 1

    print no, no_c

    count += 1
    no_c = 0

bnd = [ts[0][0],ts[0][0],ts[0][1],ts[0][1]]
for e in ts:
    if e[0] < bnd[0]:
        bnd[0] = e[0]
    elif e[0] > bnd[1]:
        bnd[1] = e[0]
    if e[1] < bnd[2]:
        bnd[2] = e[1]
    elif e[1] > bnd[3]:
        bnd[3] = e[1]
if bnd[0] > 0:
    bnd[0] *=0.9
else:
    bnd[0] *= 1.1
if bnd[1] < 0:
    bnd[1] *=0.9
else:
    bnd[1] *= 1.1
if bnd[2] > 0:
    bnd[2] *=0.9
else:
    bnd[2] *= 1.1
if bnd[3] < 0:
    bnd[3] *=0.9
else:
    bnd[3] *= 1.1

x = arange(bnd[0],bnd[1],0.1)
y = arange(bnd[2],bnd[3],0.1)
X,Y = meshgrid(x,y)
    
for j in range(n_models):
    Z = []
    for i in range(len(X)):
        z = []
        for k in range(len(X[0])):
            z.append(testpoint(X[i][k], Y[i][k], m[j]))
        Z.append(z)

    side = int(ceil(sqrt(n_models)))
    subplot(side, side, j+1)
    
    im = imshow(Z, extent=(bnd[0],bnd[1],bnd[2],bnd[3]))

d = [{},{}]
classes = []
for el in ts:
    if not d[0].has_key(el.label):
        d[0][el.label] = []
        classes.append(el.label)
    if not d[1].has_key(el.label):
        d[1][el.label] = []
    d[0][el.label].append(el[0])
    d[1][el.label].append(el[1])
#print Z
color = ['r.','b.','y.','g.']
for j in range(n_models):

    subplot(side, side, j+1)
    for c in classes:
        plot(d[0][c], d[1][c], color[classes.index(c)])
    axis(bnd)
show()
