#!/usr/bin/python
import random
import math

from ML1050.Utils.Logger import Logger
from ML1050.Utils.Enum import Enum
from ML1050.Utils.ConfusionMatrix import ConfusionMatrix
from ML1050.TrainingSet import TrainingSet
from ML1050.Example import LabeledExample
from ML1050.Classifiers.Classifier import Classifier

class NaiveBayes(Classifier):
    """
    
    """
    
    def __init__(self):
        Classifier.__init__( self)
        self.count_dict = {}
        self.num_attrs = 0
        self.num_records = 0

    def train(self, trainingSet):
        '''
        Computes posteriors and constructs dictionary that holds counts of class 
        and attribute data.
        '''
        # store training data
        self.trainingSet = trainingSet

        # store overall counts; assumes data is uniform 
        # (same number of attributes per record)
        self.num_attrs = len(self.trainingSet[0])
        self.num_records = len(self.trainingSet)
        self.num_attrs = len(self.trainingSet[0])
        self.num_records = len(self.trainingSet)

        # reset all other counts
        self.count_dict = {}

        # loop through data and update the count dictionary, which holds counts
        # of class instances and their related attribute instances
        for i in range( 0, self.num_records ):
            # update number of times class has appeared
            if ( self.count_dict.has_key( self.trainingSet[i].label ) != 1 ):
                    self.count_dict[ self.trainingSet[i].label ] = {}
                    self.count_dict[ self.trainingSet[i].label ][ 'numTotalOccurrences' ] = 1
                    self.count_dict[ self.trainingSet[i].label ][ 'attributes' ] = [ {} for attr_dict_count in range( 0, self.num_attrs ) ]
            else:
                    self.count_dict[ self.trainingSet[i].label ][ 'numTotalOccurrences' ] += 1
            # update counts for attributes
            for j in range( 0, self.num_attrs ):
                    if ( self.count_dict[ self.trainingSet[i].label ][ 'attributes' ][j].has_key( self.trainingSet[i][j] ) != 1 ):
                            self.count_dict[ self.trainingSet[i].label ][ 'attributes' ][j][ self.trainingSet[i][j] ] = 1
                    else:
                            self.count_dict[ self.trainingSet[i].label ][ 'attributes' ][j][ self.trainingSet[i][j] ] += 1

    # Classifies each record in testSet and returns a list of guessed classifications 
    def validate(self, testSet):
        # init data holders
        guessedClassifications = [] 
        trueClassifications = []

        # classify each record in testSet
        for i in range(0, len(testSet)):
            guessedClassifications.append( self.classify(testSet[i]) )
            trueClassifications.append( testSet[i].label )

        # store test data in confusion matrix
        self.confusionMatrix = ConfusionMatrix( guessedClassifications, trueClassifications)
        return self.confusionMatrix.getPercentCorrect()

    # Classifies a single data tuple/record and returns the guessed classification
    def classify(self, dataTuple):
        '''
        This method classifies a single data tuple/record and returns the guessed
        classification.
        '''
        high_post = 0
        curr_post = None
        evidence = 1
        guessed_class = None
        self.num_records = len( self.trainingSet )

        # loop through classes and find liklihood
        for c in self.count_dict.keys():
                # reset current posterior tracker to 1 so multiplying by anything would be itself first
                curr_post = 1
                for i in range( 0, self.num_attrs ):
                        if ( self.count_dict[c][ 'attributes' ][i].has_key( dataTuple[i] ) == 1 ):
                                curr_post *= ( (float)(self.count_dict[c][ 'attributes' ][i][ dataTuple[i] ] ) / self.count_dict[c][ 'numTotalOccurrences' ] )
                        else:
                                curr_post *= 1 / self.count_dict[c][ 'numTotalOccurrences' ]

                # factor in the prior
                curr_post *= ( (float)(self.count_dict[c][ 'numTotalOccurrences' ] ) / self.num_records )

                # check for new high posterior
                if ( ((float)(curr_post)) > ((float)(high_post)) ):
                        high_post = (float)(curr_post)
                        guessed_class = c
        return guessed_class
