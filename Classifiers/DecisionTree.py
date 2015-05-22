import math, sys, operator
from ML1050.Example import LabeledExample
from ML1050.TrainingSet import createTrainingSet
#from Classifier import Classifier

#class DecisionTree(Classifier) :
class DecisionTree():
    '''A decision tree classifier.
    
    Only have discrete knowledge right now.  
    need to add logic to split on a continuous value in DecisionTree._SplitAttribute
    
    '''

    def __init__(self, threshold=0.1, maxDepth=500):
        #Classifier.__init__( self)
        sys.setrecursionlimit(30000)
        
        self.threshold = threshold
        self.maxDepth = maxDepth
        self.numNodes = 0
        self.rootNode = None
        self.weights = []
    
    def train(self, trainingSet, dataWeights = []):
        """Trains a decision tree with the given trainingSet.
        
            Accepts an optional dataWeights list for Boosting. 
            """
        self.trainingSet = trainingSet
        decision = DecisionNode("root")
        for ex in trainingSet: decision.AddList(ex)
        decision.parentAttributeIndex = "null"
        decision.height = 0
        self.rootNode = decision
        self.CurrentParent = decision
        self.weights = dataWeights
        self.EntropyBefore = self.entropy(self.trainingSet)
        self._GenerateTree(self.trainingSet)        
        #print "Decision Tree trained with provided training set." 
    def test(self, example):
        return self.classify(example)
    
    def classify(self, example):
        """
        Test the DecisionTree defined by the root node
        with a single example.
        Returns the predicted class label.

        >>> from Example import LabeledExample
        >>> from TrainingSet import createTrainingSet
        >>> example3 = LabeledExample(['+', 'c', 'c', 'c', 'q'])
        >>> example4 = LabeledExample(['-', 'a', 'b', 'd', 'r'])
        >>> example5 = LabeledExample(['+', 'e', 'e', 'd', 'q'])
        >>> example6 = LabeledExample(['+', 'c', 'e', 'e', 'r'])
        >>> example7 = LabeledExample(['+', 'c', 'e', 'e', 'r'])
        >>> example8 = LabeledExample(['-', 'a', 'a', 'b', 'r'])
        >>> trainingSet = createTrainingSet([example3, example4, example5, example6, example7, example8])
        >>> testExample = LabeledExample([None, 'c', 'e', 'd', 'q'])
        >>> import DecisionTree
        >>> d = DecisionTree.DecisionTree()
        >>> d.train(trainingSet)
        >>> d.classify(testExample)
        '+'
        """
        parent = self.rootNode
        self.testExample = example
        #set the value of predictedClassLabel with the recursive function
        #_recursionclassify
        self._recursionclassify(parent)
        return self.predictedClassLabel
        
    def _recursionclassify(self, parentNode):
        """Recursively goes over the DecisionNodes in a tree until a
        leaf label is encountered.  The member variable predictedClassLabel
        is set = to the leaf label."""
        children = parentNode.GetChildren()
        splitAttribute = parentNode.attributeIndex
        exampleAttribute = self.testExample[splitAttribute]
        try:
            float(exampleAttribute)
            for child in children:
                if (float(exampleAttribute) < float(child.attribute)):
                    if child.leaf == 1:
                        #set the memeber varialbe predictedClassLabel
                        #to the leaf label of the current child
                        self.predictedClassLabel = child.leafLabel
                        return
                    else:
                        #the tree goes on...call _recurstionTest until reach a leaf
                        self._recursionclassify(child)
            # the attribute of children[0] is always the splitting value
            value = children[0].attribute
            # if the test attribute is less than the float value, go to first child
            if (float(exampleAttribute) < float(value)):
                if children[0].leaf == 1:
                    #set the memeber varialbe predictedClassLabel
                    #to the leaf label of the current child
                    self.predictedClassLabel = children[0].leafLabel
                    return
                else:
                    #the tree goes on...call _recurstionTest until reach a leaf
                    self._recursionclassify(children[0])
            # Other wise to go to second child
            else:
                if children[1].leaf == 1:
                    #set the memeber varialbe predictedClassLabel
                    #to the leaf label of the current child
                    self.predictedClassLabel = children[1].leafLabel
                    return
                else:
                    #the tree goes on...call _recurstionTest until reach a leaf
                    self._recursionclassify(children[1])
        except ValueError:
            for child in children:
                if child.attribute == exampleAttribute:
                    if child.leaf == 1:
                        #set the memeber varialbe predictedClassLabel
                        #to the leaf label of the current child
                        self.predictedClassLabel = child.leafLabel
                        return
                    else:
                        #the tree goes on...call _recurstionTest until reach a leaf
                        self._recursionclassify(child)

    def _GenerateTree(self, X):
        """ Generate a decision tree recursively """
        if self.entropy(X) <= self.threshold or self.CurrentParent.height >= self.maxDepth:
            #the CurrentParent needs to be a leaf.
            self._generateLeaf(X, self.CurrentParent)
            return
        #get the attribute to split on --> one with lowest entropy
        index = self._SplitAttribute(X)
        n=[]
        thisLevel=[]
        if self.EntropyAfter == 1.0 and self.EntropyBefore == 1.0:
            #need a leaf, this will never hit minimum threshold
            self._generateLeaf(X, self.CurrentParent)
            return
        self.EntropyBefore = self.EntropyAfter
        parent = self.CurrentParent
        # Test for index being a continuous attribute
        try:
            float(X[0][index])
            result = self._findContinuousSplit(X, index)
            splitValue = result[1]
            lesserNode = DecisionNode(splitValue)
            greaterNode = DecisionNode(sys.maxint)
            # make a decision node for values above and below splitting value
            for ex in X:
                if ex[index] < splitValue:
                    lesserNode.AddList(ex)
                else:
                    greaterNode.AddList(ex)
            if len(lesserNode.GetList()) == 0 or len(greaterNode.GetList()) == 0:
                self._generateLeaf(X, self.CurrentParent)
                return
            parent.SetAttributeIndex(index)
            lesserNode.SetParentAttributeIndex(parent.attributeIndex)
            greaterNode.SetParentAttributeIndex(parent.attributeIndex)
            lesserNode.height = parent.height + 1
            greaterNode.height = parent.height + 1
            parent.AddChildNode(lesserNode)
            parent.AddChildNode(greaterNode)
            thisLevel.append(lesserNode)
            thisLevel.append(greaterNode)
            self.numNodes += 2
            # for both nodes created at this level, call _GenerateTree
            # with the decision nodes list of examples
            for decisionNode in thisLevel:
                output = decisionNode.GetList()
                self.CurrentParent = decisionNode
                self._GenerateTree(output)
                
        except ValueError:
            #create a list of possible attributes for the current index
            for ex in X:
                if (not ex[index] in n): n.append(ex[index])
            #for each possible attribute, make a decision node 
            #and set the decision nodes member variables
            for possible in n:
                decision = DecisionNode(possible)
                for ex in X: 
                    if ex[index] == possible: decision.AddList(ex)
                parent.SetAttributeIndex(index)
                decision.SetParentAttributeIndex(parent.attributeIndex)
                decision.height = parent.height + 1
                list = decision.GetList()
                parent.AddChildNode(decision)
                thisLevel.append(decision)
                self.numNodes += 1
            #for all decision nodes created at this level, call _GenerateTree
            #with the decision nodes list of examples.  
            for decisionNode in thisLevel:
                output = decisionNode.GetList()
                self.CurrentParent = decisionNode
                self._GenerateTree(output)

    def _generateLeaf(self, X, node):
        """Find the label and generate a leaf node"""
        labels=[]
        for item in X: labels.append(item.label)
        label = leaf_label(labels)
        node.SetLeafLabel(label)
        return
    def entropy(self, trainingSet):
        """Compute the entropy of a set of examples.
    
        >>> trainingSet = createTrainingSet([])
        >>> tree = DecisionTree()
        >>> for i in range(9):
        ...  trainingSet.append(LabeledExample(['y']))
        ... 
        >>> for i in range(5):
        ...  trainingSet.append(LabeledExample(['n']))
        ... 
        >>> DecisionTree.entropy(tree,trainingSet)
        0.94028595867063092
        """
        countOfLabels = {}
        if len(self.weights) ==0:
            #print len(self.weights),len(trainingSet)
            for example in trainingSet:
                countOfLabels[example.label] = 1 + \
                countOfLabels.get(example.label, 0)
            entropy = 0
            for count in countOfLabels.values():
                p = float(count)/len(trainingSet)
                entropy -=  p * _log2(p)
        else:
            for i in range(len(trainingSet)):
                countOfLabels[trainingSet[i].label] = self.weights[i] + \
                countOfLabels.get(trainingSet[i].label, 0)
            entropy = 0
            for count in countOfLabels.values():
                p = float(count)/sum(self.weights)
                entropy -=  p * _log2(p)
        return entropy
    
    def _findContinuousSplit(self, trainingSet, index):
        # sort all the values, and map values to their labels
        trainingSet.sort(key = operator.itemgetter(index))
        
        entropy = sys.maxint
        previousLabel = trainingSet[0].label
        previousValue = trainingSet[0][index]
        for record in trainingSet:
            # splitting points will only happen when labels change
            # between consecutive values
            value = record[index]
            if record.label != previousLabel:
                currentEntropy = 0
                splittingValue = previousValue + (value - previousValue) / 2
                lessThan = []
                greaterThan = []
                # split the training set into groups greater than
                # and less than the splitting value
                for record2 in trainingSet:
                    if record2[index] < splittingValue:
                        lessThan.append(record2)
                    else:
                        greaterThan.append(record2)
                # find entropy of split
                e = float(len(lessThan))/len(trainingSet) *\
                        self.entropy(lessThan)
                e += float(len(greaterThan))/len(trainingSet) *\
                        self.entropy(greaterThan)
                # If this is the best entropy so far, store it
                if e < entropy:
                    entropy = e
                    finalValue = splittingValue
            previousValue = value
            previousLabel = record.label
        # return both the entropy and the splitting value
        result = [entropy, finalValue]
        return result


    def _SplitAttribute(self, X):
        """ Decide which attribute to split on.
        Only have discrete knowledge for now. """
        bestf = None    # The best feature to split on
        MinInt = sys.maxint
        example = X[0]
        i=0
        entropyList=[]
        while( i < len(example) ):
            try:
                # Test if this is continuous, and if it is find the best
                # split
                float(example[i])
                result = self._findContinuousSplit(X,i)
                if result[0] < MinInt:
                    MinInt = result[0]
                    bestf = i
            except ValueError:
                n=[]
                #get a list of possible attributes to split on
                for ex in X:
                    if(not (ex[i]) in n): n.append(ex[i])
                E = 0
                #loop through all possible attributes 
                for possible in n:
                    decision=[]
                    #decision = DecisionNode(possible)
                    for ex in X:
                        if ex[i] == possible: decision.append(ex)
                    DecisionLists = decision
                    e = float(len(DecisionLists))/len(X) *\
                    self.entropy(DecisionLists)
                    E += e
                if E < MinInt:
                    MinInt = E
                    bestf = i
            self.EntropyAfter = MinInt
            i+=1
        return bestf

    def PrintTree(self, parentNode):
            """Call with parent node.
            Kryptic print not in tree form but
            can reconstruct tree on paper.
            Used when debugging GenerateTree recursion"""
            print parentNode

    def __call__(self, example):
        """
            Calling an instance like a function is used to test a new 
        example.
        
        >>> from Example import LabeledExample
        >>> from TrainingSet import createTrainingSet
        >>> example3 = LabeledExample(['+', 'c', 'c', 'c', 'q'])
        >>> example4 = LabeledExample(['-', 'a', 'b', 'd', 'r'])
        >>> example5 = LabeledExample(['+', 'e', 'e', 'd', 'q'])
        >>> example6 = LabeledExample(['+', 'c', 'e', 'e', 'r'])
        >>> example7 = LabeledExample(['+', 'c', 'e', 'e', 'r'])
        >>> example8 = LabeledExample(['-', 'a', 'a', 'b', 'r'])
        >>> trainingSet = createTrainingSet([example3, example4, example5, example6, example7, example8])
        >>> testExample = LabeledExample([None, 'c', 'e', 'd', 'q'])
        >>> import DecisionTree
        >>> d = DecisionTree.DecisionTree()
        >>> d.train(trainingSet)
        >>> d(testExample)
        '+'
        """
        return self.classify(example)

class DecisionNode:

    def __init__(self, attribute):
        """attribute is the value that came down this path""" 
        self.parentAttributeIndex = 0
        self.attribute = attribute
        self.taken=[]
        self.attributeIndex = 0
        self.leafLabel = ""
        self.Children=[]
        self.leaf = 0
        self.height = 0
 
    def AddList(self, example):
        """adds an example to the nodes that have taken this route"""
        self.taken.append(example)

    def GetList(self):
        """returns a list of examples that have taken this route"""
        return self.taken

    def SetAttributeIndex(self, index):
        """the index of the attribute that this node split on"""
        self.attributeIndex = index

    def SetParentAttributeIndex(self, index):
        """the index of the attribute that the parent of this
        node split on"""
        self.parentAttributeIndex = index

    def SetLeafLabel(self, label):
        """if this node is a leaf, set the label and the value of leaf
        to be true"""
        self.leafLabel = label
        self.leaf = 1

    def AddChildNode(self, child):
        """adds a DecisionNode to the list of this nodes children.
        Children keeps track of each nodes children."""
        self.Children.append(child)

    def GetChildren(self):
        """returns the list of children nodes for this DecisionNode"""
        return self.Children

    def __repr__(self):
            string = "<Index parent node split on: "
            string += str(self.parentAttributeIndex)
            string += ", Attribute from parent split: "
            string += str(self.attribute)
            string += ", height: "
            string += str(self.height)
            if self.leaf == 1:
                    string += ', Leaf label: '
                    string += str(self.leafLabel)
            else:
                    string += ', Index children split on: '
                    string += str(self.attributeIndex)
            string += ">"
            outputStr = "\n"
            for i in range(self.height): outputStr += "\t"
            outputStr += string
            for child in self.Children: outputStr += child.__repr__()
            return outputStr

def _log2(x):
    """ Compute the log (base 2 of a number).

    >>> _log2(1)
    0.0
    >>> _log2(2)
    1.0
    >>> _log2(4)
    2.0
    >>> _log2(32)
    5.0
    >>> _log2(10)
    3.3219280948873626
    """
    
    return math.log(x)/math.log(2)



def leaf_label(class_list):
    """Return the majority class of a list of classes"""
    count ={}
    for field in class_list:
        count_of_label = count.get(field, 0)
        count[field] = count_of_label + 1
    max = 0
    for item in count.keys():
        if count[item] > max:
            max = count[item]
            label = item
    return label
    
def _classify():
    """Run the tests in the documentation strings."""
    import doctest
    return doctest.testmod(verbose=True)
    
if __name__ == "__main__":
    try:
        __IP                # Are we running IPython?
    except NameError:
        _classify()             # If not, run the tests



