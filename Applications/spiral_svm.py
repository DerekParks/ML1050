"""
Application: spiral_svm.py

Training Dataset: N/A
    
Description: Creates a spiral and uses SVMs to sparate the two classes.

How to Run: python Applications/spiral_svm.py (from root ML1050 directory)
"""

from ML1050.External.SVM import SVM
from ML1050.Preprocessing.CrossValidation import kFold
from ML1050.Example import LabeledExample
from ML1050.TrainingSet import *
from math import *
import Image
import sys, csv, getopt, copy 

def main():
    #create a 600 by 600 image
    SIZE=600
    
    image = Image.new('RGB',(SIZE,SIZE))

    
    #populate a list of examples that are in a spiral shape
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
    
    print 'Made',len(genpoints),'points'
    trainingSet = createTrainingSet(genpoints)
    
    SVMmodel = SVM(kernelType = 'RBF',svm_type = 'C_SVC', probability = 1)
    SVMmodel.train(trainingSet)
    
    for i in range(SIZE):
        for j in range(SIZE):
            example = LabeledExample([i,j],label=0)
            colMod,colPrb = SVMmodel.prob(example)
            color=(int(255*colPrb[-100]),int(255*colPrb[100]),0)
            #print colMod,colPrb
            #color=(100,0,0)
            #if colMod < 0:
                #color=(0,100,0)
            image.putpixel((i,j),color)
    
    #print trainingSet
    for data in trainingSet:
        loc = (roundOff(data[0]),roundOff(data[1]))
        #print "at", loc
        if data.label == -100:
            image.putpixel(loc,(0,255,0))
        else:
            image.putpixel(loc,(255,0,0))
    image.save("img.bmp")

def translate(r,theta):
        return (r*cos(theta),r*sin(theta))
def magnitude(xy):
        return sqrt(xy[0]**2+xy[1]**2)
def incTheta(theta):
        return theta + 20*pi/180
def roundOff(input):
        return int(round(input))
def shift(xy,size):
        '''take the given point, and shift them to a centered placement'''
        return (xy[0]+size/2,xy[1]+size/2)
def _test():
    """Run all tests by docstring"""
    import doctest
    return doctest.testmod(verbose=False)

if __name__ == "__main__":
    try:
        __IP
    except NameError:
        _test()
    main()
    
