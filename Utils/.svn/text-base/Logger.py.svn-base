"""
The Logger is used to easily output debug messages for the coder as well as provide easy access to file output. Debug levels increase in levels of severity. A debug level of 0 would be used if the output is part of the general output of the program (i.e. a confusion matrix). As the complexity of the program increases, additional debug messages can be added with a severity of the message diminishing with the increase of the debug level. For example, a debug level of 1 would generally be used to show severe debug messages that won't be output to the user (i.e. exceptions), whereas a debug level of 3 would be used to output the entrance into a loop or simple tracers. The debug levels also output any previous debug levels (so a debug level of 1 would show severe debug messages and standard output).
The idea is that by simply turning the debug level of the logger to 3 the coder can see all possible output and easily trace through and fix any issues.
Separate files could be used to display separate aspects of the program and the coder can use "tail -f <file name>" to view changes in an organized fashion.
"""
class Logger(object):
    """
    Example Usage:

    >>> log = Logger(2,3)
    >>> log.write("Hello",0,"Logger > write()")
    ( Logger > write() ) Hello
    >>> list = [1,2,3,4]
    >>> log.writeList(list, 0, "/", "Logger > writeList()") 
    ( Logger > writeList() ) 1 / 2 / 3 / 4 / 
    >>> log.writeOut("Test", 0, 0, "", "Logger > writeOut()")
    ( Logger > writeOut() ) Test
    ( Logger: writeToFile ) ERROR: The file name is not valid!
    >>> log.writeListOut(list, 0, 0, "", ",", "Logger > writeListOut")
    ( Logger > writeListOut ) 1 , 2 , 3 , 4 , 
    ( Logger: writeListToFile ) ERROR: The file name is not valid!
    >>> log.setDebugLevel(0)
    >>> log.setFileDebugLevel(0)
    >>> log.getDebugLevel()
    0
    >>> log.getFileDebugLevel()
    0
    >>> log.write("Hello",1,"Logger > write()")
    >>> log.writeList(list, 1, "/", "Logger > writeList()") 
    >>> log.writeOut("Test", 1, 1, "", "Logger > writeOut()")
    >>> log.writeListOut(list, 1, 1, "", ",", "Logger > writeListOut")
    >>> log.setDebugLevel('a')
    >>> log.setFileDebugLevel('a')
    >>> log.getDebugLevel()
    0
    >>> log.getFileDebugLevel()
    0
    """
    def __init__( self, debugLevel, fileDebugLevel) :
        """
        Constructor
        debugLevel: The debug level for standard output
        fileDebugLevel: The debug level for all file output
        """    
        if(debugLevel < 0):
            debugLevel = 0
        if(fileDebugLevel < 0):
            fileDebugLevel = 0
        self.debugLevel = debugLevel
        self.fileDebugLevel = fileDebugLevel

    def write(self, message, debugLevel, source = ""): 
        """
        Writes a debug message to standard output
        message: The message to output
        debugLevel: The debug level of the message
        source (optional): Displays the class and method used to display the message (i.e. "Logger: write" if this method called the write on the log)
        """
        if(self.debugLevel >= debugLevel):
            if(len(source) > 0):
                print "(",source,")",    
            print message
    
    def writeToFile(self, message, debugLevel, fileName, source = ""):
        """
        Writes a debug message to a file
        message: The message to write
        debugLevel: The debug level of the message
        fileName: The file to write to. It will be created if it does not exist
        source (optional): Displays the class and method used to display the message (i.e. "Logger: writeToFile" if this method called the write on the log)
        """
        if(fileName== "" or not isinstance(fileName, str)):
            self.write("ERROR: The file name is not valid!",1,"Logger: writeToFile")
        elif(self.fileDebugLevel >= debugLevel):
            f = open(fileName, 'a')    
            if(len(source) > 0):
                f.write('(')
                f.write(source)
                f.write(') ')
            f.write(message)
            f.write('\n')
            f.close()

    def writeOut(self, message, debugLevel, fileDebugLevel, fileName, source = ""):
        """
        Writes a message to stdout and to a file
        """
        self.write(message, debugLevel, source)
        self.writeToFile(message, fileDebugLevel, fileName, source)        


    def writeList(self, myList, debugLevel, delimiter = " ", source=""): 
        """
        Outputs lists in a user specific manner.
        myList: The list to output
        debugLevel: The debug level for the list
        delimiter: The delimiter used to separate the values in the list (i.e. a delimiter value of "," would create the output 1,2,3, from list [1,2,3])
        source (optional): Displays the class and method used to display the message (i.e. "Logger: writeList" if this method called the write on the log)
        """
        if(not isinstance(myList,list)):
            self.write("ERROR: not a list!",1,"Logger: writeList")
        elif(self.debugLevel >= debugLevel):
            if(len(source) > 0):
                print "(",source,")",    
            for i in myList:
                print i,delimiter,
            print ""

    def writeListToFile(self, myList, debugLevel, fileName, delimiter = " ", source=""): 
        """
        Outputs lists in a user specific manner.
        myList: The list to output
        debugLevel: The debug level for the list
        fileName: The file to append to
        delimiter: The delimiter used to separate the values in the list (i.e. a delimiter value of "," would create the output 1,2,3, from list [1,2,3])
        source (optional): Displays the class and method used to display the message (i.e. "Logger: writeListToFile" if this method called the write on the log)
        """
        if(not isinstance(myList,list)):
            self.write("ERROR: not a list!",1,"Logger: writeListToFile")
        elif(fileName== "" or not isinstance(fileName, str)):
            self.write("ERROR: The file name is not valid!",1,"Logger: writeListToFile")
        elif(self.fileDebugLevel >= debugLevel):
            f = open(fileName, 'a')    
            if(len(source) > 0):
                f.write('(')
                f.write(source)
                f.write(') ')
            for i in myList:
                f.write(str(i))
                f.write(delimiter)        
            f.write('\n')
            f.close()

    def writeListOut(self, myList, debugLevel, fileDebugLevel, fileName, delimiter = " ", source=""): 
        """
        Writes a list to stdout and to the file
        """
        self.writeList(myList, debugLevel, delimiter, source)
        self.writeListToFile(myList, fileDebugLevel, fileName, delimiter, source)
    def setDebugLevel(self, debugLevel):
        """
        Mutator for debug level. 
        The debug level must be an int and must be greater than 0
        """
        if(isinstance(debugLevel, int) and debugLevel >= 0):
            self.debugLevel = debugLevel

    def setFileDebugLevel(self, fileDebugLevel):
        """
        Mutator for file debug level.
        The debug level must be an int and must be greater than or equal to 0
        """
        if(isinstance(fileDebugLevel, int) and fileDebugLevel >= 0):
            self.fileDebugLevel = fileDebugLevel 

    def getDebugLevel(self):
        """
        Accessor for debug level
        """
        return self.debugLevel

    def getFileDebugLevel(self):
        """
        Accessor for file debug level
        """
        return self.fileDebugLevel 
