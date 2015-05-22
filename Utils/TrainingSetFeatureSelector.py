"""
    Selects specific features of an element, or 
    set of elements in a TrainingSet.
"""
from ML1050.Example import LabeledExample
from ML1050.TrainingSet import TrainingSet

def removeExampleFeatures(example, removeList):
    """Removes features provided in a list of indicies from an example.
    
    >>> from ML1050.Example import LabeledExample
    >>> from ML1050.TrainingSet import TrainingSet
    >>> from ML1050.Utils.TrainingSetFeatureSelector import removeExampleFeatures
    >>> example = LabeledExample([0,'zero','one','two','three'])
    >>> print example
    <label: 0, input: ['zero', 'one', 'two', 'three']>
    >>> removeExampleFeatures(example, [1,3])
    >>> print example
    <label: 0, input: ['zero', 'two']>
    """
    offset = 0
    originalExampleSize = len(example)
    for i in range(originalExampleSize):
        if i in removeList:
            del example[i-offset]
            offset = offset + 1
        
def keepExampleFeatures(example, keepList):
    """Keeps features provided in a list of indicies from an example.
    All the rest are removed
    
    >>> from ML1050.Example import LabeledExample
    >>> from ML1050.TrainingSet import TrainingSet
    >>> from ML1050.Utils.TrainingSetFeatureSelector import keepExampleFeatures
    >>> example = LabeledExample([0,'zero','one','two','three'])
    >>> print example
    <label: 0, input: ['zero', 'one', 'two', 'three']>
    >>> keepExampleFeatures(example, [1,3])
    >>> print example
    <label: 0, input: ['one', 'three']>
    """
    offset = 0
    originalExampleSize = len(example)
    for i in range(originalExampleSize):
        if i not in keepList:
            del example[i-offset]
            offset = offset + 1
    
def selectExampleFeatures(example, patternList):
    """Keeps features provided in provided pattern

    >>> from ML1050.Example import LabeledExample
    >>> from ML1050.TrainingSet import TrainingSet
    >>> from ML1050.Utils.TrainingSetFeatureSelector import selectExampleFeatures
    >>> example = LabeledExample([0,'zero','one','two','three'])
    >>> print example
    <label: 0, input: ['zero', 'one', 'two', 'three']>
    >>> selectExampleFeatures(example, [0,1,0,1])
    >>> print example
    <label: 0, input: ['one', 'three']>
    """
    if len(patternList) != len(example):
        raise Exception, "Pattern does not match example"

    offset = 0
    originalExampleSize = len(example)
    for i in range(originalExampleSize):
        if patternList[i] != 0 and patternList[i] != 1:
            raise Exception, "Invalid pattern format"
        if patternList[i] == 0:
            del example[i-offset]
            offset = offset + 1
            
def removeTrainingSetFeatures(trSet, removeList):
    """Removes features features provided in a list of indicies 
    from all examples in a TrainingSet
    
    >>> from ML1050.Example import LabeledExample
    >>> from ML1050.TrainingSet import TrainingSet
    >>> from ML1050.Utils.TrainingSetFeatureSelector import removeTrainingSetFeatures
    >>> e1 = LabeledExample([0,0,1,2,3])
    >>> e2 = LabeledExample([1,4,5,6,7])
    >>> ts = TrainingSet()
    >>> ts.append(e1)
    >>> ts.append(e2)
    >>> removeTrainingSetFeatures(ts,[1])
    >>> print ts
    [<label: 0, input: [0, 2, 3]>, <label: 1, input: [4, 6, 7]>]
    
    """
    for e in trSet:
        removeExampleFeatures(e,removeList)
        
def keepTrainingSetFeatures(trSet, keepList):
    """Keeps features features provided in a list of indicies 
    from all examples in a TrainingSet.  All other features are removed.
    
    >>> from ML1050.Example import LabeledExample
    >>> from ML1050.TrainingSet import TrainingSet
    >>> from ML1050.Utils.TrainingSetFeatureSelector import keepTrainingSetFeatures
    >>> e1 = LabeledExample([0,0,1,2,3])
    >>> e2 = LabeledExample([1,4,5,6,7])
    >>> ts = TrainingSet()
    >>> ts.append(e1)
    >>> ts.append(e2)
    >>> keepTrainingSetFeatures(ts,[1])
    >>> print ts
    [<label: 0, input: [1]>, <label: 1, input: [5]>]
    
    """
    for e in trSet:
        keepExampleFeatures(e, keepList)
        
def selectTrainingSetFeatures(trSet, patternList):
    """Keeps features provided in provided pattern.

    >>> from ML1050.Example import LabeledExample
    >>> from ML1050.TrainingSet import TrainingSet
    >>> from ML1050.Utils.TrainingSetFeatureSelector import selectTrainingSetFeatures
    >>> e1 = LabeledExample([0,0,1,2,3])
    >>> e2 = LabeledExample([1,4,5,6,7])
    >>> ts = TrainingSet()
    >>> ts.append(e1)
    >>> ts.append(e2)
    >>> selectTrainingSetFeatures(ts,[1,1,0,0])
    >>> print ts
    [<label: 0, input: [0, 1]>, <label: 1, input: [4, 5]>]

    """
    for e in trSet:
        selectExampleFeatures(e, patternList)
    
    
def _test():
    """Run the tests in the documentation strings."""
    import doctest
    return doctest.testmod(verbose=True)

if __name__ == "__main__":
    try:
        __IP                            # Are we running IPython?
    except NameError:
        _test()                         # If not, run the tests