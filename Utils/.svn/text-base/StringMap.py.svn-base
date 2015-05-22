from ML1050.Example import LabeledExample

class StringMapper:
    def __init__(self, referenceSet):
        self.labelMap = {}
        self.labelCount = 0
        self.attributeMap = [None]*len(referenceSet[0])
        self.attributeCount = [0]*len(referenceSet[0])
        #check all attributes, and lets find the ones that need numberification
        self.doMap = [x for x in range(len(referenceSet[0])) if self.stringTest(referenceSet[0][x]) == True]
        # do all of them ??
        #self.doMap = [x for x in range(len(referenceSet[0]))]
        self.doLabel = self.stringTest(referenceSet[0].label)
        
        self.set = True
        
        for index in self.doMap:
            self.attributeMap[index] = {}
        
        #trapdoor. we dont need to do all this work, if the data is fine as is;
        # however, this seems to mess it up 
        #so we're actually skipping it for the moment
        '''
        if self.doLabel == False and sum(self.doMap) == 0:
            self.set = False
            return
            '''
        
        #translate em all
        for element in referenceSet:
            #check the label
            if self.doLabel:
                if self.conditionalDictAdd(self.labelMap,element.label,self.labelCount):
                    self.labelCount += 1
            for index in self.doMap:
                if self.conditionalDictAdd(self.attributeMap[index],element[index],self.attributeCount[index]):
                    self.attributeCount[index] += 1
        #print self.labelMap,self.attributeMap
        
    def map(self,input):
        if self.set:
            #return new label
            if (input.label == None):
                newLabel = None
            else:
                if self.conditionalDictAdd(self.labelMap,input.label,self.labelCount):
                    self.labelCount += 1
                newLabel = self.labelMap[input.label]
            newData = input[:]
            for index in self.doMap:
                if self.conditionalDictAdd(self.attributeMap[index],newData[index],self.attributeCount[index]):
                    self.attributeCount[index] += 1
                newData[index]=self.attributeMap[index][input[index]]
            ex = LabeledExample(newData,label=newLabel)
            return ex       
        else:
            #sanitize
            ex = LabeledExample([self.convertToNative(x) for x in input[:]],label=self.convertToNative(input.label))
            return ex

    def revMapLabel(self,input):
        if self.set:
            return self.labelMap.keys()[self.labelMap.values().index(int(input))]
        else:
            return input
        
    def conditionalDictAdd(self,hashtable,key,value):
        if not hashtable.has_key(key):
            hashtable[key]=value
            return True
        return False
        
            
    def stringTest(self,object):
        try:
            float(object)
            #it is a num
            return False
        except ValueError:
            #sneaky string
            return True
    def convertToNative(self,object):
        if object == None:
            return None
        try:
            return int(object)
        except ValueError:
            try:
                return float(object)
            except ValueError:
                #if you get here, something is bad.
                return object
 
