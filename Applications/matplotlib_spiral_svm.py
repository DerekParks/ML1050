from pylab import *
from ML1050.External.SVM import SVM
from ML1050.TrainingSet import createTrainingSet
from ML1050.Example import LabeledExample
import copy

m = SVM()

def incTheta(theta):
    return theta + 20*pi/180
def shift(xy,size):
    '''take the given point, and shift them to a centered placement'''
    return (xy[0]+size/2,xy[1]+size/2)
def translate(r,theta):
    return (r*cos(theta),r*sin(theta))
def testpoint(x,y):
    #prd,ret = m.prob(LabeledExample([x,y],label=None))
    #return ret[prd]
    return m.test(LabeledExample([x,y],label=None))



#populate a list of examples that are in a spiral shape
SIZE = 600
maxMag = sqrt(SIZE**2+SIZE**2)    
theta = 0
r1 = 0
r2 = 0
a = 1
b = 1
genpoints = []
for i in range(60):
    theta = incTheta(theta)
    r1 =12*theta #spiral
    r2 =-12*theta #spiral2
    posPoint = shift(translate(r1,theta),SIZE)
    negPoint = shift(translate(r2,theta),SIZE)
    posExample = LabeledExample([posPoint[0],posPoint[1]], label = 100)
    negExample = LabeledExample([negPoint[0],negPoint[1]], label = -100)
    genpoints.append(posExample)
    genpoints.append(negExample)
ts = createTrainingSet(genpoints)
m.train(ts)

x = arange(0,600,2)
y = arange(600,0,-2)
X,Y = meshgrid(x,y)
Z = copy.copy(X)
for i in range(len(Z)):
    for k in range(len(Z[0])):
        Z[i][k] = testpoint(X[i][k],Y[i][k])

im = imshow(Z, extent=(0,600,0,600))
"""
xt = {}
yt = {}
for i in range(SIZE/2):
    for j in range(SIZE/2):
        ex = LabeledExample([2*i,2*j],label=None)
        p = m.test(ex)
        if not xt.has_key(p):
            xt[p] = []
        if not yt.has_key(p):
            yt[p] = []
        xt[p].append(ex[0])
        yt[p].append(ex[1])
plot(xt[100], yt[100], 'r.')
plot(xt[-100], yt[-100], 'b.')
"""

x = {}
y = {}
for el in ts:
    if not x.has_key(el.label):
        x[el.label] = []
    if not y.has_key(el.label):
        y[el.label] = []
    x[el.label].append(el[0])
    y[el.label].append(el[1])
plot(x[100], y[100], 'ro')
plot(x[-100], y[-100], 'bo')
show()
