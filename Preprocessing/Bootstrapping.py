#!/usr/bin/evn python

"""An implementation of boostraping."""

import random

def bootstrap(inputData, numBootstraps=10):
    """Yield training and validation pairs of boostrapped samples from
    the inputData.

    The training set is chosen with replacement, and
    the validation set is chosen as those examples not picked for the
    training set.

    Training and validation pairs are yielded through a generator.
    Use it like this:

    >>> from TrainingSet import TrainingSet
    >>> training = TrainingSet('Datasets/votes-train0.csv')
    >>> len(training)
    347
    >>> for t,v in bootstrap(training, numBootstraps=10):
    ...     print len(t) == len(training) and len(v) < len(training)
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
    for i in range(numBootstraps):
        training = []
        for i in range(len(inputData)):
            training.append(random.choice(inputData))
        validation = [ example for example in inputData
                       if example not in training ]
        yield training, validation


def _test():
    """Run the tests in the documentation strings."""
    import doctest
    return doctest.testmod(verbose=True)
    
if __name__ == "__main__":
    try:
        __IP                            # Are we running IPython?
    except NameError:
        _test()                         # If not, run the tests

