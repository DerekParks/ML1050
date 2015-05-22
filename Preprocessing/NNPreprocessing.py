from ML1050.TrainingSet import TrainingSet
from ML1050.Example import LabeledExample

class NNPreprocessing:
    """
    The NNPreprocessing class will transform inputs or class labels 
    from discrete strings to vectors
    
    So a class label with possible values a,b,c will get mapped to [1,0,0], [0,1,0], [0,0,1] respectively 
    
    Create a TrainingSet with string inputs and class labels
    >>> trainingSet = TrainingSet()
    >>> trainingSet.append(LabeledExample(['y','x'], label = 'a'))
    >>> trainingSet.append(LabeledExample(['n','y'], label = 'b'))
    >>> trainingSet.append(LabeledExample(['y','z'], label = 'c'))
    >>> trainingSet.append(LabeledExample(['n','z'], label = 'aa'))
    >>> trainingSet.append(LabeledExample(['n','x'], label = 'a'))
    
    Creating NNPreprocessing with a TrainingSet and other arguments default will process both inputs
    and class labels 
    
    >>> myNNPre = NNPreprocessing(trainingSet)

    Now look at trainingSet 
    
    >>> trainingSet[0]
    <label: [1, 0, 0, 0], input: [0, 0, 1, 0]>
    
    Notice 'a' became [1, 0, 0, 0] and ['y','x'] became [1, 0, 0, 1, 0]
    Look at a couple of other examples to be sure everything is working
    
    >>> trainingSet[1]
    <label: [0, 0, 0, 1], input: [1, 1, 0, 0]>
    
    >>> trainingSet[2]
    <label: [0, 0, 1, 0], input: [0, 0, 0, 1]>
    
    >>> trainingSet[3]
    <label: [0, 1, 0, 0], input: [1, 0, 0, 1]>
    
    >>> trainingSet[4]
    <label: [1, 0, 0, 0], input: [1, 0, 1, 0]>
    
    Now lets transform trainingSet back into string labels and inputs
    
    >>> myNNPre(trainingSet)
    
    Now all examples should be back the way they started
    
    >>> trainingSet[0]
    <label: a, input: ['y', 'x']>
    
    >>> trainingSet[1]
    <label: b, input: ['n', 'y']>
    
    >>> trainingSet[2]
    <label: c, input: ['y', 'z']>
    
    >>> trainingSet[3]
    <label: aa, input: ['n', 'z']>
    
    >>> trainingSet[4]
    <label: a, input: ['n', 'x']>
    
    NNPreprocessing will also try to convert class labels 
    from a string to a list with a single int or float
    
    Testing with an int label
    >>> trainingSet = TrainingSet()
    >>> trainingSet.append(LabeledExample([1,1], label = '1'))

    Only convert labels
    >>> myNNPre = NNPreprocessing(trainingSet, True, False)
    >>> trainingSet[0].label
    [1]
    >>> myNNPre(trainingSet)
    >>> trainingSet[0].label
    '1'
    
    Testing with a float label
    >>> trainingSet = TrainingSet()
    >>> trainingSet.append(LabeledExample([1,1], label = '1.1'))
    
    Again only convert labels
    >>> myNNPre = NNPreprocessing(trainingSet, True, False)
    >>> trainingSet[0].label
    [1.1000000000000001]
    >>> myNNPre(trainingSet)
    >>> trainingSet[0].label
    '1.1'
    
    
    Test with a different encoding
    >>> trainingSet = TrainingSet()
    >>> trainingSet.append(LabeledExample(['y','x'], label = 'a'))
    >>> trainingSet.append(LabeledExample(['n','y'], label = 'b'))
    >>> trainingSet.append(LabeledExample(['y','z'], label = 'c'))
    >>> trainingSet.append(LabeledExample(['n','z'], label = 'aa'))
    >>> trainingSet.append(LabeledExample(['n','x'], label = 'a'))

    >>> myNNPre = NNPreprocessing(trainingSet, encoding=[-1, 1])
    >>> trainingSet[0]
    <label: [1, -1, -1, -1], input: [-1, -1, 1, -1]>
    >>> trainingSet[1]
    <label: [-1, -1, -1, 1], input: [1, 1, -1, -1]>
    >>> trainingSet[3]
    <label: [-1, 1, -1, -1], input: [1, -1, -1, 1]>

    Test reversing
    >>> myNNPre(trainingSet)
    >>> trainingSet[0]
    <label: a, input: ['y', 'x']>
    >>> trainingSet[1]
    <label: b, input: ['n', 'y']>
    >>> trainingSet[2]
    <label: c, input: ['y', 'z']>
    
    
    Test having a test set with examples not in the training set 
    
    Use the same trainset as above
    >>> myNNPre = NNPreprocessing(trainingSet)
    
    Create a test set that has values not seen in the training set
    >>> testSet = TrainingSet()
    >>> testSet.append(LabeledExample(['y','n'], label = 'd'))
    >>> testSet.append(LabeledExample(['n','y'], label = 'b'))
    >>> testSet.append(LabeledExample(['y','z'], label = 'c'))
    >>> testSet.append(LabeledExample(['n','z'], label = 'aa'))
    >>> testSet.append(LabeledExample(['n','p'], label = 'e'))
    >>> myNNPre.forward(testSet)
    >>> testSet[0]
    <label: [0, 0, 0, 0], input: [0, 0, 0, 0]>
    >>> testSet[1]
    <label: [0, 0, 0, 1], input: [1, 1, 0, 0]>
    >>> testSet[2]
    <label: [0, 0, 1, 0], input: [0, 0, 0, 1]>
    
    Note: There is currently no functionality to map a test set with unseen values back to its orginal state.
    
    
    Test forceStr option
    >>> trainingSet = TrainingSet()
    >>> trainingSet.append(LabeledExample([0,0], label = 1))
    >>> trainingSet.append(LabeledExample([1,1], label = 0))
    >>> myNNPre = NNPreprocessing(trainingSet, expandTwo = True, forceStr=True)
    >>> trainingSet[0]
    <label: [1, 0], input: [0, 1, 0, 1]>
    """
    def __init__(self,trainingSet, doLabels = True, doInputs = True, expandTwo = False, encoding = [0,1],forceStr=False):
        """
        trainingSet - the TrainingSet to be transformed
        doLabels - if True class labels will be converted
        doInputs - if True class inputs will be converted
        expandTwo - if False variables with only 2 options will be encoded as 0 or 1
                    if True they will be encoded as [0 1] or [1 0]
        encoding - A list of two items which tells how examples will be converted. The first item will be 
                    used when the output is False and the 2nd when it is True. The default is [0, 1]
        forceStr - Will force ints and floats to a string before doing normal encoding
        """
        self.inputMappings = None
        self.labelMappings = None
        self.encoding = encoding
        self.expandTwo = expandTwo
        self.forceStr = forceStr
        if(len(self.encoding) != 2):
            raise ValueError, 'encoding list must have 2 items' 
        
        if self.forceStr:
            self.trainingSetToStrings(trainingSet, doInputs, doLabels)
            
        if(doInputs):
            self.inputMappings = self.toVectorInputs(trainingSet)
            
        if(doLabels):
            self.labelMappings = self.toVectorLabels(trainingSet) 
   
    def __call__(self, trainingSet):
        self.back(trainingSet)
        
    def trainingSetToStrings(self, trainingSet, doInputs, doLabels):
        if(doInputs):
            for i in range(len(trainingSet)):
                trainingSet[i]= LabeledExample([str(x) for x in trainingSet[i]] , label = trainingSet[i].label)
            
        if(doLabels):
            for i in range(len(trainingSet)):
                trainingSet[i].label = str(trainingSet[i].label)         

    def forward(self, trainingSet):
        """Map another trainingSet, such as a test set, based on saved mapping to vectors"""
        doInputs = self.inputMappings is not None
        doLabels = self.labelMappings is not None
        
        if self.forceStr:
            self.trainingSetToStrings(trainingSet, doInputs, doLabels)        
        
        if doInputs:
            self.toVectorInputsFromMapping(trainingSet,self.inputMappings)
        
        if doLabels:       
            self.toVectorLabelsFromMapping(trainingSet, self.labelMappings)
        
    def back(self, trainingSet):
        """Map trainingSet back to strings"""
        if self.inputMappings is not None:
            self.toStrInputs(trainingSet,self.inputMappings)
        
        if self.labelMappings is not None:
            self.toStrLabels(trainingSet, self.labelMappings)
            
    def toVectorInputs(self, trainingSet):
        mappingAllIns = [dict() for i in range(len(trainingSet[0]))]
        
        for ex in trainingSet:
            for i,item in enumerate(ex):
                mappingAllIns[i][item]=""
          
        for uniqueIn in mappingAllIns:
            for i,label in enumerate(uniqueIn):
                uniqueIn[label] = i 

        self.toVectorInputsFromMapping(trainingSet, mappingAllIns)
        
        return mappingAllIns
    
    def toVectorInputsFromMapping(self, trainingSet, mappingAllIns):
        for i in range(len(trainingSet)):
            newInput = list()
                 
            for j,item in enumerate(trainingSet[i]):
                if len(mappingAllIns[j]) == 2 and not self.expandTwo:
                    try:
                        newInput.append(self.encoding[mappingAllIns[j][item]])
                    except KeyError:
                        raise ValueError, 'There is a class encoded as a two class problem that has 3 possible values. Try again with expandTwo=True' 
                else:
                    try:
                        newInput.extend(self.numberToVec(mappingAllIns[j][item], len(mappingAllIns[j])))
                    except KeyError:
                        newInput.extend( [self.encoding[0]] * len(mappingAllIns[j]))
                
            trainingSet[i] = LabeledExample(newInput, label=trainingSet[i].label)
    
    def toStrInputs(self, trainingSet, mappingIns):

        reversedMappings = [ dict(zip(oneMapping.values(), oneMapping.keys())) for oneMapping in mappingIns ]
        
        for k in range(len(trainingSet)):
            newInput = []
            
            i = 0
            j = 0
            
            for oneMapping in reversedMappings:
                lenOneMapping = len(oneMapping)
                
                if lenOneMapping == 2:
                    j += 1
                    newInput.append(oneMapping[self.encodingToIndex(trainingSet[k][i])])
                    i += 1
                else:
                    j += lenOneMapping
                    newInput.append(oneMapping[self.vecToNumber(trainingSet[k][i:j])])
                    i += lenOneMapping
                    
            trainingSet[k] = LabeledExample(newInput, label=trainingSet[k].label)
                
    def encodingToIndex(self, item):
        if self.encoding[0] == item:
            return 0
        else:
            return 1
    
    def toVectorLabels(self, trainingSet):
        stringsFound = self.forceStr #if self.forceStr is true already know everything is a string
        floatsFound = False
        intsFound = False
        
        if not self.forceStr:
            for ex in trainingSet:
                try:
                    int(ex.label)
                    intsFound = True
                except ValueError:
                    try:
                        float(ex.label)
                        floatsFound = True
                    except ValueError:
                        stringsFound = True
        
        #print intsFound, floatsFound, stringsFound
        if(floatsFound and not stringsFound) :
            for example in trainingSet:
                example.label=[float(example.label)]
            return -1
            
        elif(intsFound and not stringsFound and not floatsFound):
            for example in trainingSet:
                example.label=[int(example.label)]
            return -1
            
        else:
            #find all unique classes
            classLabels = dict([(ex.label,"") for ex in trainingSet])
        
            for i,label in enumerate(classLabels):
                classLabels[label] = i 

            self.toVectorLabelsFromMapping(trainingSet, classLabels)

            return classLabels
        
    def toVectorLabelsFromMapping(self, trainingSet, classLabels): 
        if len(classLabels) == 2 and not self.expandTwo:
            for example in trainingSet:
                try:
                    example.label = [self.encoding[classLabels[example.label]]]
                except KeyError:
                    raise ValueError, 'There is a class encoded as a two class problem that has 3 possible values. Try again with expandTwo=True'
        else:
            for example in trainingSet:
                try:
                    example.label = self.numberToVec(classLabels[example.label], len(classLabels))
                except KeyError:
                    example.label = [self.encoding[0]] * len(classLabels)
    
    def toStrLabels(self, trainingSet, classLabels=None):
        if classLabels == -1 :
            for ex in trainingSet:
                ex.label = str(ex.label[0])
         
        else:
            #use some tricksy python to reverse the keys and values 
            newClassLabels = dict(zip(classLabels.values(), classLabels.keys()))

            if len(newClassLabels) == 2 and not self.expandTwo:
                for example in trainingSet:
                    example.label = newClassLabels[self.encodingToIndex(example.label[0])]
            else:
                for example in trainingSet:
                    example.label = newClassLabels[self.vecToNumber(example.label)]
    
    def numberToVec(self, i, len):
        """
        >>> NNPreprocessing(None,False,False).numberToVec(2,5)
        [0, 0, 1, 0, 0]
        """
        vec = [self.encoding[0]] * len
        vec[i] = self.encoding[1]

        return vec
    
    def vecToNumber(self, vec):
        """
        >>> NNPreprocessing(None,False,False).vecToNumber([0,1,0])
        1
        """
        numLabel = None
        for i,el in enumerate(vec):
            if el == self.encoding[1]:
                numLabel = i
                break
        
        if numLabel == None:    
            raise ValueError, 'Cannot map a training set back to orginal state that has values not seen in the training set passed to the constructor'
        return numLabel

def _test():
    """Run the tests in the documentation strings."""
    import doctest
    return doctest.testmod(verbose=True)

    
def _test2():
    trainingSet = TrainingSet()
    trainingSet.append(LabeledExample([0,0], label = '0'))
    trainingSet.append(LabeledExample([1,1], label = '1'))
    myNNPre = NNPreprocessing(trainingSet, expandTwo = True, forceStr=True)
    print trainingSet[0]

if __name__ == "__main__":
    try:
        __IP                            # Are we running IPython?
    except NameError:
        _test()                         # If not, run the tests            
        #_test2()    