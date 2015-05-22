
class LabeledExample(list):
    """The LabeledExample class holds a single training/testing
    example.

    An example has two parts: (1) a class label (the required output);
    and (2) the input vector represented as a list.  The class
    inherits from the built-in list type, and this is the list where
    it stores the input vector.

    Examples can be created two ways.  If you pass the constructor a
    single list, it takes the first item as the class label and the
    rest as the input vector.  For example,

    >>> ex = LabeledExample(['2', '2.050', '230'])
    >>> ex.label
    '2'

    This should make it easy to create training examples from CSV
    files.

    The second way to create examples is to specify a label in the
    constructor with the 'label' keyword:

    >>> ex2 = LabeledExample([4, 5, 5.2], label='red')
    >>> ex2.label
    'red'

    Examples print themseleves out in a somewhat verbose way.
    >>> ex
    <label: 2, input: ['2.050', '230']>
    >>> ex2
    <label: red, input: [4, 5, 5.2000000000000002]>

    You can even specify None as a label.

    >>> ex3 = LabeledExample([7, 'b', 8, 3.1], label=None)
    >>> ex3
    <label: None, input: [7, 'b', 8, 3.1000000000000001]>
    >>> ex3.label
    >>> str(ex3.label)
    'None'

    Notice that LabeledExamples act just like lists, which is often
    what you want:

    >>> ex4 = LabeledExample([9, 10, 'f', 'g', 8,], label=True)
    >>> for input in ex4:
    ...     print input
    ... 
    9
    10
    f
    g
    8
    >>> ex5 = LabeledExample(['y', 5, 6, 7, 8, 9, 10])
    >>> ex5
    <label: y, input: [5, 6, 7, 8, 9, 10]>
    >>> len(ex5)
    6
    >>> 9 in ex5
    True
    """
    def __init__(self, exampleAsList, **kwargs):
        # Check to see if the label was specified as a keyword
        # argument.  If it was use it, not the first element of the
        # input list.
        if kwargs.has_key("label"):
            self.label = kwargs["label"]
            # If the label is explicitly specified, use the whole list
            # as the input vector.
            inputList = exampleAsList  
        else:
            self.label = exampleAsList[0]
            # If we take the label as the first element element, use
            # the remaining elements as the input vector.
            inputList = exampleAsList[1:]
        super(LabeledExample, self).__init__(inputList)

    def __repr__(self):
        """Labeled examples know how to print themseleves out.
        
        """
        return "<label: %s, input: %s>" % (self.label,
                                         super(LabeledExample, self).__repr__())

def _test():
    """Run the tests in the documentation strings."""
    import doctest
    return doctest.testmod(verbose=True)
    
if __name__ == "__main__":
    try:
        __IP                            # Are we running IPython?
    except NameError:
        _test()                         # If not, run the tests
