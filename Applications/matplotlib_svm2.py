from pylab import *
from ML1050.TrainingSet import TrainingSet
from ML1050.Example import LabeledExample
from ML1050.External.SVM import SVM
from random import random

def testpoint(x,y, mod):
    return int(mod.test(LabeledExample([x,y],label=None)))

ts = TrainingSet('../Datasets/bishop_synthetic.csv')
#m = SVM(kernelType = 'RBF', C = 100, gamma = 0.5, svm_type = 'C_SVC')
#m.train(ts)

m = []
n_models = 2
count = 0
no_c = 0 # count the number it gets correct to evaluate the model parameters
for i in range(n_models):
    for j in range(n_models):
        Nu = float(i+1)/n_models - 0.1
        Gamma = float(j)/n_models
        m.append(SVM(kernelType = 'RBF', svm_type = 'NU_SVC', 
            nu = Nu, gamma = Gamma))
        m[count].train(ts)

        for s in ts:
            if testpoint(s[0], s[1], m[count]) == float(s.label):
                no_c += 1

        print Nu, Gamma, no_c

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
#Z = [[[0]*len(X[0])]*len(X)]*(n_models**2)
    
for j in range(n_models**2):
    Z = []
    for i in range(len(X)):
        z = []
        for k in range(len(X[0])):
            #z.append(testpoint(bnd[0] + random()*(bnd[1] - bnd[0]), 
                    #bnd[2] + random()*(bnd[3] - bnd[2]), m[j]))
            z.append(testpoint(X[i][k], Y[i][k], m[j]))
        Z.append(z)

    subplot(n_models, n_models, j+1)
    
    #figure(j)
    #im = imshow(Z[j], extent=(bnd[0],bnd[1],bnd[2],bnd[3]))
    im = imshow(Z, extent=(bnd[0],bnd[1],bnd[2],bnd[3]))
"""
for j in range(n_models**2):
    for i in range(len(Z[0])*len(Z[0][0])):
        Z[j][i/len(Z[0])][i%len(Z[0])] = testpoint(bnd[0] + 
            random()*(bnd[1]-bnd[0]), bnd[2] + random()*(bnd[3]-bnd[2]), m[j])
"""

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
for j in range(n_models**2):

    subplot(n_models, n_models, j+1)
    #figure(j)
    for c in classes:
        plot(d[0][c], d[1][c], color[classes.index(c)])
    axis(bnd)
show()
