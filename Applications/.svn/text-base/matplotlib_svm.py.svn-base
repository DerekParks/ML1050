from pylab import *
from ML1050.TrainingSet import TrainingSet
from ML1050.Example import LabeledExample
from ML1050.External.SVM import SVM

def testpoint(x,y, mod):
    return mod.test(LabeledExample([x,y],label=None))

ts = TrainingSet('../Datasets/bishop_synthetic.csv')
m = SVM(kernelType = 'RBF', C = 10, gamma = 0.4, svm_type = 'C_SVC')
m.train(ts)

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
Z = [[0]*len(X[0])]*len(X)
for i in range(len(Z)):
    for k in range(len(Z[0])):
        Z[i][k] = testpoint(X[i][k], Y[i][k], m)
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

color = ['b.','r.','y.','g.']
for c in classes:
    plot(d[0][c], d[1][c], color[classes.index(c)])
axis(bnd)
show()
