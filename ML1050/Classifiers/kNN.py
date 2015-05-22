
"""An implementation of a k-nearest neighbor classifier."""

import random
from ML1050.Classifiers import classifier as _classifier

class kNN(_classifier):
    """A kNN classifer.

    In the example below, we create a k=1 nearest neighbor classifer
    that measures the distance between examples as the number of
    discrete features that don't match.  We train the classifier on
    two training examples and test it on a third.

    >>> from ML1050.Example import LabeledExample
    >>> from ML1050.TrainingSet import createTrainingSet
    >>> example1 = LabeledExample(['y', 'a', 'a', 'a'])
    >>> example2 = LabeledExample(['n', 'b', 'b', 'b'])
    >>> trainingSet = createTrainingSet([example1, example2])
    >>> testExample = LabeledExample([None, 'a', 'a', 'b'])
    >>> def d(ex1, ex2):
    ...     dist = len(ex1)
    ...     for i in range(len(ex1)):
    ...        if ex1[i] == ex2[i]:
    ...            dist -= 1
    ...     return dist
    ...
    >>> k = kNN(1, d)
    >>> k.train(trainingSet)
    >>> k.test(testExample)
    'y'

    """
    def __init__(self, k, distanceFunction):
        self.k = k
        self.dist = distanceFunction
        self.distances = {}

    def train(self, trainingSet):
        """Training is trivial for kNN.  Just store the training set."""
        self.trainingSet = trainingSet

    def test(self, testExample):
        for example in self.trainingSet:
            d = self.dist(example, testExample)
            # Keep all the examples that are the same distance away in a
            # list that is keyed by that distance.
            distList = self.distances.get(d, [])
            distList.append(example)
            self.distances[d] = distList
        # Now find the closest examples to the testExample
        sortedDists = self.distances.keys()
        sortedDists.sort()
        kNearestNeighbors = []
        neighborsNeeded = self.k
        for d in sortedDists:
            neighborsAtD = self.distances[d]
            if len(neighborsAtD) < neighborsNeeded:
                kNearestNeighbors.extend(neighborsAtD)
                neighborsNeeded -= len(neighborsAtD)
                if neighborsNeeded == 0:
                    break
            else:                       # We have more neighbors than we need
                random.shuffle(neighborsAtD)
                kNearestNeighbors.extend(neighborsAtD[0:neighborsNeeded])
                break
        # Each of the k nearest neighbors gets a vote
        votes = {}
        for neighbor in kNearestNeighbors:
            votes[neighbor.label] = votes.get(neighbor.label, 0) + 1
        listOfVotes = [ (num, label) for label, num in votes.items() ]
        listOfVotes.sort()
        numVotes, classLabel = listOfVotes[-1]
        return classLabel
            
    def __call__(self, example):
        """
        Calling an instance like a function is used to test a new example

        >>> from ML1050.Example import LabeledExample
        >>> from ML1050.TrainingSet import createTrainingSet
        >>> example3 = LabeledExample(['+', 'c', 'c', 'c', 'q'])
        >>> example4 = LabeledExample(['-', 'a', 'b', 'd', 'r'])
        >>> example5 = LabeledExample(['+', 'e', 'e', 'd', 'q'])
        >>> example6 = LabeledExample(['+', 'c', 'e', 'e', 'r'])
        >>> example7 = LabeledExample(['+', 'c', 'e', 'e', 'r'])
        >>> example8 = LabeledExample(['-', 'a', 'a', 'b', 'r'])
        >>> trainingSet = createTrainingSet([example3, example4, example5, example6, example7, example8])
        >>> testExample = LabeledExample([None, 'c', 'e', 'd', 'q'])
        >>> def d(ex1, ex2):
        ...     dist = len(ex1)
        ...     for i in range(len(ex1)):
        ...        if ex1[i] == ex2[i]:
        ...            dist -= 1
        ...     return dist
        ...
        >>> k = kNN(3, d)
        >>> k.train(trainingSet)
        >>> k(testExample)
        '+'
        """
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

