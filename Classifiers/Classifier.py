"""An implementation of a general classifier."""

import cPickle
import random
import math

from ML1050.Utils.ConfusionMatrix import ConfusionMatrix
from ML1050.Utils.Logger import Logger
from ML1050.Utils.Enum import Enum
from ML1050.TrainingSet import TrainingSet
from ML1050.Example import LabeledExample

class Classifier :

    """A generic classifier.
    
    Only requires non-generic classifiers to specifiy how to train and classify
    data.  Testing and validation is taken care of.
    
    """

    def __init__(self) :
        """
        The constructor only initializes a logger. The rest is up to the actual
        classifiers.  Because of they way confusion matrix class is written,
        one will only be generated in methods which return them.
        """
        self.confusionMatrix = ConfusionMatrix( [], [])
        self.logger = Logger(2,2)
        self.trainingSet = None
        
    def train(self, trainingSet) :
        pass

    def classify(self, element) :
        pass
        
    def test(self, dataSet) :
        """
        This method receives a data set and records the classifies each element in
        the data set according to the classifier's classification standards and
        methods.
        """
        
        testValues = [len(dataSet)]
        for i in range(len(dataSet)) :
            testValues[i] = self.classify(dataSet[i])
        return testValues
        
    def trainValidate(self, validationSet, threshold) :
        """
        This method receives a data set and trains the classifier on the data set.
        The threshold (a decimal percentage) serves as a determination of how much
        of the given data set to train on and how much should be used for
        validation.  Finally, this method returns a confusion matrix.
        """
        
        # Determine training set size
        thresholdSize = (int)(len( data ) * threshold)
        
        # Create training set
        tSet = data[0:thresholdSize]
        
        # Create validation set
        vSet = data[thresholdSize:len(data)]
        
        # Train
        self.train(self, tSet)
        
        # Determine correct labels / predicted values and classify each element
        pValues = [len(vSet)]
        vValues = [len(vSet)]
        for i in range(len(vSet)) :
            pValues[i] = vSet[i][0]
            vValues[i] = self.classify(vSet[i])
        
        return ConfusionMatrix(pValues, tValues)

    def serialize(self, filename) :
        """
        Accepts a filename and saves classifier to that file.
        """
        outfile = open( filename, "wb")
        cPickle.dump( self, outfile)
        outfile.close()
