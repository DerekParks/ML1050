"""An implementation of a bagging algorithm taking a Classifier and a number, representing the number
  of instances of the classifier to run bagging on.
  This class also implements bootstrapping to generate the training sets for the replicated classifiers. 

"""

import random
import copy

class Bagging:
    """A Bagging class.

    When we test Fisher Linear Discriminant we need to import parts of the ML1050 library
    >>> from Classifiers import DecisionTree
    >>> from Example import LabeledExample
    >>> from ML1050.TrainingSet import TrainingSet
    >>> from TrainingSet import createTrainingSet
    >>> from Classifiers import Bagging
    >>> from Classifiers.Bagging import Bagging

    Create a data set with character labels and inputs
    >>> data = TrainingSet()
    >>> data.append(LabeledExample(['n', 'n', 'y', 'n', 'n', 'n', 'y', 'y', 'y', 'n', 'n', 'n', 'n', 'n', 'y', 'y'], label = 'D'))
    >>> data.append(LabeledExample(['y', 'y', 'y', 'n', 'n', 'y', 'y', 'y', 'y', 'y', 'y', 'y', 'y', 'y', 'n', 'y'], label = 'D'))
    >>> data.append(LabeledExample(['y', 'y', 'y', 'n', 'y', 'y', 'n', 'y', 'n', 'n', 'y', 'n', 'y', 'n', 'y', 'y'], label = 'D'))
    >>> data.append(LabeledExample(['n', 'y', 'y', 'n', 'n', 'y', 'y', 'y', 'y', 'y', 'y', 'n', 'y', 'y', 'y', 'y'], label = 'D'))
    >>> data.append(LabeledExample(['y', 'n', 'y', 'n', 'y', 'y', 'y', 'n', 'n', 'n', 'y', 'n', 'n', 'y', 'n', 'y'], label = 'D'))
    >>> data.append(LabeledExample(['y', 'y', 'y', 'n', 'n', 'y', 'y', 'y', 'n', 'n', 'y', 'y', 'n', 'y', 'n', 'y'], label = 'D'))
    >>> data.append(LabeledExample(['n', 'y', 'y', 'n', 'y', 'y', 'n', 'y', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'y'], label = 'D'))
    >>> data.append(LabeledExample(['y', 'n', 'y', 'n', 'n', 'y', 'y', 'y', 'y', 'y', 'n', 'y', 'n', 'y', 'n', 'y'], label = 'D'))
    >>> data.append(LabeledExample(['y', 'y', 'y', 'n', 'n', 'n', 'y', 'y', 'y', 'n', 'y', 'n', 'n', 'n', 'y', 'y'], label = 'D'))
    >>> data.append(LabeledExample(['y', 'n', 'y', 'n', 'n', 'y', 'n', 'y', 'y', 'y', 'y', 'y', 'y', 'n', 'n', 'y'], label = 'D'))
    >>> data.append(LabeledExample(['y', 'n', 'n', 'n', 'n', 'n', 'y', 'y', 'y', 'y', 'n', 'n', 'n', 'y', 'n', 'y'], label = 'R'))
    >>> data.append(LabeledExample(['y', 'y', 'n', 'y', 'y', 'y', 'n', 'n', 'n', 'y', 'y', 'n', 'y', 'n', 'n', 'n'], label = 'R'))
    >>> data.append(LabeledExample(['n', 'y', 'n', 'y', 'y', 'y', 'n', 'n', 'n', 'y', 'n', 'y', 'y', 'y', 'n', 'y'], label = 'R'))
    >>> data.append(LabeledExample(['n', 'n', 'n', 'y', 'y', 'y', 'y', 'y', 'y', 'y', 'n', 'y', 'y', 'y', 'n', 'y'], label = 'R'))
    >>> data.append(LabeledExample(['n', 'y', 'n', 'y', 'y', 'y', 'n', 'n', 'n', 'y', 'y', 'y', 'y', 'y', 'n', 'n'], label = 'R'))
    >>> data.append(LabeledExample(['y', 'n', 'n', 'y', 'y', 'n', 'y', 'y', 'y', 'n', 'n', 'y', 'y', 'y', 'n', 'y'], label = 'R'))
    >>> data.append(LabeledExample(['n', 'y', 'n', 'y', 'y', 'y', 'n', 'y', 'n', 'n', 'n', 'y', 'y', 'y', 'n', 'y'], label = 'R'))
    >>> data.append(LabeledExample(['n', 'y', 'y', 'y', 'y', 'y', 'y', 'n', 'y', 'y', 'n', 'y', 'y', 'y', 'n', 'y'], label = 'R'))
    >>> data.append(LabeledExample(['n', 'y', 'n', 'y', 'y', 'y', 'n', 'n', 'n', 'n', 'n', 'y', 'y', 'y', 'n', 'n'], label = 'R'))
    >>> data.append(LabeledExample(['n', 'n', 'n', 'y', 'y', 'n', 'n', 'n', 'n', 'n', 'n', 'y', 'n', 'y', 'n', 'y'], label = 'R'))
    >>> data.append(LabeledExample(['n', 'n', 'n', 'y', 'y', 'y', 'n', 'n', 'n', 'y', 'n', 'y', 'y', 'y', 'n', 'y'], label = 'R'))

    A test example to check the bagging classifier
    >>> testExample = LabeledExample([None, 'n', 'n', 'n', 'y', 'y', 'y', 'n', 'n', 'n', 'y', 'n', 'y', 'y', 'y', 'n', 'y'])
    
    The classifier we will use to test bagging.  Note you can use any classfier you like with baggging
    >>> d = DecisionTree.DecisionTree()
    
    Create a bagging classfier, which will include 20 decision tree models
    >>> bagger = Bagging(d,20)
    
    Train the bagging classifier
    >>> bagger.train(data)
    
    Test the bagging classifier on the test example
    >>> bagger.test(testExample)
    'R'

    You can also run Bagging with classifiers that give arguments at each train call as well,
    so long as trainingSet is the first argument.
    """

    def __init__(self, classifier, n=10):
        """
        Each member of the classifier list is expected to be able to use
        every member of the trainingSet in order to train itself.
        """

        self.classifierList = []

        for i in range (0,n):
            self.classifierList.append(copy.copy(classifier))


    def train(self, trainingSet, *argv):#added argv unpacking, to be called with classifier.train
        """ Train each classifier on the training set """
        for classifier in self.classifierList:
            training = []
            for i in range(len(trainingSet)):
                        training.append(random.choice(trainingSet))
            classifier.train(training, *argv)
        
    def test(self, testExample, *argv): #added argv unpacking, to be called with classifier.test
        self.dictionary = {}
        """ Tests a new input using the classifiers """
        for classifier in self.classifierList:
            x = classifier.test(testExample, *argv)
            if self.dictionary.has_key(x):
                self.dictionary[x]=self.dictionary[x]+1
            else:
                self.dictionary[x]=1
        
        winningLabel = self.dictionary.keys()[0]
        winningCount = self.dictionary[self.dictionary.keys()[0]]
        for key in self.dictionary.keys():
            if self.dictionary[key]>winningCount:
                winningLabel = key
                winningCount = self.dictionary[key]

        return winningLabel

    def __call__(self, example):
        return self.test(example)       
            
def _test():
    """Run the tests in the documentation strings."""
    import doctest
    return doctest.testmod(verbose=True) 

if __name__ == "__main__":
        try:
                __IP                            # Are we running IPython?
        except NameError:
                _test()                         # If not, run the tests

