#!/usr/bin/python

"""Implements k-fold cross-validiation and Ditterch's 5x2
cross-validiation method.
"""

import random

def _buildFolds(inputData, k=10):
    """Return a list of folds.  Each fold is a list of examples.

     The
    inputData must be list-like, meaning that it's type can be the
    built-in list or a TrainingSet, which inherits from list.  The
    return value is a list of k folds, where the union of all the k
    folds is the whole inputData.

    >>> from ML1050.TrainingSet import TrainingSet
    >>> training = TrainingSet('Datasets/votes-train0.csv')
    >>> folds = _buildFolds(training)
    >>> len(folds)
    10
    >>> [ len(fold) for fold in folds ]
    [35, 35, 35, 35, 35, 35, 35, 34, 34, 34]
    >>> sum([ len(fold) for fold in folds ])
    347
    >>> sum([ len(fold) for fold in folds ]) == len(training)
    True

    """
    # make a copy of the data set so that we don't shuffle original data
    data = inputData[:]
    random.shuffle(data)
    # Initialize the folds to empty lists
    folds = []
    for i in range(k):
        folds.append([])
    # Loop over data and build up the folds
    for i in range(len(data)):
        index = i % k
        folds[index].append(data[i])
    return folds

def kFold(inputData, k=10):
    """This is the traditional k-fold cross-validiation method.

    It is implemented as a generator, so loop through it like so:

    >>> for training, validation in kFold(range(10)):
    ...     print len(training), len(validation)
    ... 
    9 1
    9 1
    9 1
    9 1
    9 1
    9 1
    9 1
    9 1
    9 1
    9 1

    >>> from ML1050.TrainingSet import TrainingSet
    >>> training = TrainingSet('Datasets/votes-train0.csv')
    >>> for t,v in kFold(training, k=5):
    ...     t.extend(v); print t.sort() == training.sort()
    ... 
    True
    True
    True
    True
    True
    """
    uniqueFolds = _buildFolds(inputData, k)
    for i in range(k):
        training = []
        validation = []
        for j in range(k):
            if i != j:
                training.extend(uniqueFolds[j])
            else:
                validation.extend(uniqueFolds[j])
        yield training, validation
        

def ditterch5x2(inputData):
    """Create Ditterch's 5x2 cross validation set.

    Performs 2-fold cross-valdiation 5 times. Of the 2 folds, each one
    is used as the training set once, while the other is used as the
    validation set.  10 training/validation pairs are yielded through
    a generator.

    >>> from ML1050.TrainingSet import TrainingSet
    >>> training = TrainingSet('Datasets/votes-train0.csv')
    >>> len(training)
    347
    >>> for t,v in ditterch5x2(training):
    ...     print len(t), len(v)
    ... 
    174 173
    173 174
    174 173
    173 174
    174 173
    173 174
    174 173
    173 174
    174 173
    173 174
    >>> for t,v in ditterch5x2(training):
    ...     t.extend(v); print t.sort() == training.sort()
    ... 
    True
    True
    True
    True
    True
    True
    True
    True
    True
    True
    
    """
    for i in range(5):
        fold1, fold2 = _buildFolds(inputData, k=2)
        yield fold1, fold2
        yield fold2, fold1

# Some more tests                    
__test__ = {
    "simple-buildFolds" : """
    >>> folds = _buildFolds(range(32))
    >>> len(folds)
    10
    >>> [ len(fold) for fold in folds ]
    [4, 4, 3, 3, 3, 3, 3, 3, 3, 3]
    >>> sum([ 19 in fold for fold in folds ])
    1
    >>> sum([ sum(fold) for fold in folds ]) == sum(range(32))
    True
    """,
    "simple-kFold" : """
    >>> for t,v in kFold(range(102), 20):
    ...     print len(t), len(v)
    ... 
    96 6
    96 6
    97 5
    97 5
    97 5
    97 5
    97 5
    97 5
    97 5
    97 5
    97 5
    97 5
    97 5
    97 5
    97 5
    97 5
    97 5
    97 5
    97 5
    97 5
    
    >>> from ML1050.TrainingSet import TrainingSet
    >>> training = TrainingSet('Datasets/titanic.csv')
    >>> for t,v in kFold(training, k=30):
    ...    print len(t), len(v)
    ... 
    2127 74
    2127 74
    2127 74
    2127 74
    2127 74
    2127 74
    2127 74
    2127 74
    2127 74
    2127 74
    2127 74
    2128 73
    2128 73
    2128 73
    2128 73
    2128 73
    2128 73
    2128 73
    2128 73
    2128 73
    2128 73
    2128 73
    2128 73
    2128 73
    2128 73
    2128 73
    2128 73
    2128 73
    2128 73
    2128 73
    >>> for t,v in kFold(training, k=30):
    ...    print len(t) + len(v) == len(training)
    ... 
    True
    True
    True
    True
    True
    True
    True
    True
    True
    True
    True
    True
    True
    True
    True
    True
    True
    True
    True
    True
    True
    True
    True
    True
    True
    True
    True
    True
    True
    True
    """,
}

def _test():
    """Run the tests in the documentation strings."""
    import doctest
    return doctest.testmod(verbose=True)
    
if __name__ == "__main__":
    try:
        __IP                            # Are we running IPython?
    except NameError:
        _test()                         # If not, run the tests

