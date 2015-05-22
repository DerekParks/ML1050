
import csv
import tempfile
from Example import LabeledExample

class TrainingSet(list):
    """The TrainingSet class holds a list of training examples.

    The class is created from a CSV file.  Every row in the CSV file
    is converted into a LabeledExample class, and every labeled
    example is added to the TrainingSet.

    >>> training = TrainingSet('Datasets/NBA_TRAIN.csv')
    >>> training[0]
    <label: 2, input: [2.0499999999999998, 230]>
    >>> example = training[0]
    >>> example.label
    '2'
    >>> example
    <label: 2, input: [2.0499999999999998, 230]>
    >>> example[0]
    2.0499999999999998
    >>> example[1]
    230

    TrainingSet acts like a list, which has some nice features.

    >>> len(training)
    373
    >>> training[0:5]
    [<label: 2, input: [2.0499999999999998, 230]>, <label: 2, input: [2.0, 250]>, <label: 2, input: [1.9750000000000001, 210]>, <label: 1, input: [1.825, 168]>, <label: 2, input: [2.0249999999999999, 245]>]

    >>> for example in training[0:5]:
    ...     print example[0]
    ... 
    2.05
    2.0
    1.975
    1.825
    2.025

    >>> [ example.label for example in training[0:5] ]
    ['2', '2', '2', '1', '2']

    Notice that the TrainingSet constructor automatically converts the
    input values to ints or floats if possible.  (Remember that
    everything read from a CSV file is a string.) Add the keyword
    parameter autoConvertDataTypes=False to the constructor if your
    data set has ints or floats that you would like to keep as strings.

    >>> stringTraining = TrainingSet('Datasets/NBA_TRAIN.csv', autoConvertDataTypes=False)
    >>> stringTraining[0]
    <label: 2, input: ['2.050', '230']>
    >>> example = stringTraining[20]
    >>> type(example[0])
    <type 'str'>

    See the _autoConvert docstring for more information.
    """
    
    def __init__(self, filename=None, autoConvertDataTypes=True, **kwargs):
        """Any kwargs are passed to the csv reader construtor.  For example,
        when the data are separtated by spaces instead of a comma:
        >>> brokenTraining = TrainingSet('Datasets/mushroom-with-spaces.train')
        >>> brokenTraining[0]
        <label: p f s g t f f c b p t b f f w w p w o p h v u, input: []>
        >>> brokenTraining[0].label
        'p f s g t f f c b p t b f f w w p w o p h v u'
        
        all the data gets stuck in the label.  But the csv module can handle 
        this data with the right keyword argument:
        
        >>> fixedTraining = TrainingSet('Datasets/mushroom-with-spaces.train', delimiter=' ')
        >>> fixedTraining[0]
        <label: p, input: ['f', 's', 'g', 't', 'f', 'f', 'c', 'b', 'p', 't', 'b', 'f', 'f', 'w', 'w', 'p', 'w', 'o', 'p', 'h', 'v', 'u']>
        >>> fixedTraining[0].label
        'p'
        
        """
        # TrainingSet is empty with no filename
        if not filename:
            return
        csvreader = csv.reader(file(filename), **kwargs)
        for row in csvreader:
            if row[0][0] != '#':    # skip comment lines. assumes no blank lines
                self.append(LabeledExample(row))
        # If requested, try to convert input values to ints or floats
        if autoConvertDataTypes:
            self._autoConvert()
            
    def _autoConvert(self):
        """Convert all the input values from string to int or float,
        if possible.

        Because the TrainingSet is created from a CSV file, all the
        data types are strings.  Usually, the file contains ints and
        floats, and it would be nice if they were converted
        automatically.

        >>> training = TrainingSet('Datasets/NBA_TRAIN.csv')
        >>> example = training[5]
        >>> example
        <label: 2, input: [1.95, 230]>
        >>> example[0]
        1.95
        >>> example[1]
        230
        >>> type(example[1])
        <type 'int'>
        >>> type(example[0])
        <type 'float'>
        
        Notice that the label of the example is never converted.

        >>> example.label
        '2'
        >>> type(example.label)
        <type 'str'>

        
        """
        for example in self:
            for i in range(len(example)):
                try:
                    example[i] = int(example[i])
                except ValueError:
                    try:
                        example[i] = float(example[i])
                    except ValueError:
                        pass        # Leave it as a string

        
def createTrainingSet(iterable, autoConvertDataTypes=True):
    """Factory method to create training sets from lists and other
    iterables.

    >>> example1 = LabeledExample([5, 6, 7, 8], label='y')
    >>> example2 = LabeledExample(['1', '2.5', '3.1', 4], label='n')
    >>> trainingSet = createTrainingSet([example1, example2])
    >>> trainingSet
    [<label: y, input: [5, 6, 7, 8]>, <label: n, input: [1, 2.5, 3.1000000000000001, 4]>]
    >>> len(trainingSet)
    2
    >>> for ex in trainingSet:
    ...     print ex.label
    ... 
    y
    n

    """
    trainingSet = TrainingSet();
    for example in iterable:
        trainingSet.append(example)
    if autoConvertDataTypes:
        trainingSet._autoConvert()
    return trainingSet

# Some more tests                    
__test__ = {
    "votes-data" : """
    >>> training = TrainingSet('Datasets/votes-train0.csv')
    >>> len(training)
    347
    >>> dems = [ example for example in training if example.label == 'D' ]
    >>> len(dems)
    213
    >>> repb = [ example for example in training if example.label == 'R' ]
    >>> len(repb)
    134
    """,
    "titanic-data" : """
    >>> training = TrainingSet('Datasets/titanic.csv')
    >>> len(training)
    2201
    >>> training[0]
    <label: yes, input: ['1st', 'adult', 'male']>
    >>> children = [ example for example in training if example[1] == 'child' ]
    >>> len(children)
    109
    >>> adults = [ example for example in training if example[1] == 'adult' ]
    >>> len(adults)
    2092
    >>> len(training) == len(children) + len(adults)
    True
    """
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

