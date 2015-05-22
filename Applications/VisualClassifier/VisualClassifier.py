import os
import wx
from pylab import *
from ML1050.TrainingSet import TrainingSet
from ML1050.External.SVM import SVM
from ML1050.TrainingSet import TrainingSet
from ML1050.Example import LabeledExample
from random import random

from Test import *
from Shim import *

class VisualClassifier(wx.Frame):
    
    MID_ABOUT = 101
    MID_EXIT = 110
    
    trainingSet = None
    
    def __init__(self,parent,id,title):
        #init window
        wx.Frame.__init__(self,parent,wx.ID_ANY,title, size= (500,500))
        #init status bar
        self.CreateStatusBar()
        #set up bar menu
        barmenu = [None]*1
        barmenu[0]= wx.Menu()
        barmenu[0].Append(self.MID_ABOUT, "&About"," Program information")
        barmenu[0].AppendSeparator()
        barmenu[0].Append(self.MID_EXIT, "E&xit", " Exit the program")
        #create the bar menu
        menu = wx.MenuBar()
        menu.Append(barmenu[0],"&File")
        self.SetMenuBar(menu)
        
        notebook = wx.Notebook(self,-1)
        
        self.form1 = self.Form1(notebook,-1,self)
        self.form2 = self.Form2(notebook,-1,self)
        self.form3 = self.Form3(notebook, -1, self)
        notebook.AddPage(self.form1, "Step 1: Data Selection")
        notebook.AddPage(self.form2, "Step 2: Test Selection")
        notebook.AddPage(self.form3, "Step 3: Results")
        
        
        #attach event handlers
        wx.EVT_MENU(self, self.MID_ABOUT, self.OnAbout)
        wx.EVT_MENU(self, self.MID_EXIT, self.OnExit)
        
        
        self.Show(True)
    def OnAbout(self,e):
        d= wx.MessageDialog( self, " GUI for Classifiers, using wxPython","About VisualClassifier", wx.OK)
        d.ShowModal()
        d.Destroy()
    def OnExit(self,e):
        self.Close(True)
    
    
    class Form1(wx.Panel):
        EID_LOAD = 10
        EID_GRAPH = 11
        appRef = None
        def __init__(self, parent, id, appRef):
            wx.Panel.__init__(self, parent, id)
            self.appRef = appRef
            self.welcome = wx.StaticText(self, -1, "Welcome to the VisualClassifier",wx.Point(20,30))
            self.button =wx.Button(self, self.EID_LOAD, "Load Dataset", wx.Point(100, 125))
            self.plotButton = wx.Button(self, self.EID_GRAPH, "Plot", wx.Point(200, 125))
            self.plotButton.Enable(False)
            self.stat = wx.TextCtrl(self,5, "",wx.Point(100,200), wx.Size(300,200),wx.TE_MULTILINE | wx.TE_READONLY)
            wx.EVT_BUTTON(self, self.EID_LOAD, self.fileChoose)
            wx.EVT_BUTTON(self, self.EID_GRAPH, self.graph)
        def graph(self,e):
            pframe = self.graphPanel(self.appRef)
           
            pframe.Refresh()
        def fileChoose(self,e):
            dir = os.path.join(os.path.split(os.path.split(os.path.abspath(os.path.curdir))[0])[0],"Datasets")
            opener = wx.FileDialog(self, "Choose a data file", dir, "", "*.*", wx.OPEN)
            opener.ShowModal()
            try:
                self.appRef.trainingSet = TrainingSet(os.path.join(opener.GetDirectory(),opener.GetFilename()))
                self.plotButton.Enable(True)
                self.button.SetLabel("Change")
                self.stat.AppendText("Loaded: "+opener.GetFilename()+"\n")
                self.stat.AppendText(" Has %i examples\n" % len(self.appRef.trainingSet))
            except IOError:
                pass
            except:
                d= wx.MessageDialog( self, "An error has occured. Please make sure the file is in the correct format.","Unable to load file", wx.OK)
                self.stat.AppendText("Unable to open: "+opener.GetFilename()+"\n")
                d.ShowModal()
                d.Destroy()
            opener.Destroy()
            
        
        class graphPanel(wx.Frame):
            appRef = None
            def __init__(self,appRef):
                self.appRef = appRef
                wx.Frame.__init__(self,None,wx.ID_ANY,"Plot", size= (500,500))
                self.graph()
                self.Show(True)
            def graph(self):
                try:
                    d = [{},{}]
                    classes = []
                    for el in self.appRef.trainingSet:
                        if not d[0].has_key(el.label):
                            d[0][el.label] = []
                            classes.append(el.label)
                        if not d[1].has_key(el.label):
                            d[1][el.label] = []
                        d[0][el.label].append(el[0])
                        d[1][el.label].append(el[1])
    
                    color = ['r.','b.','y.']
                    clf()
                    for c in classes:
                        plot(d[0][c], d[1][c], color[classes.index(c)])
                    savefig("fig.jpg", dpi=60)
                    self.bitmap = wx.Bitmap("fig.jpg")
                    wx.EVT_PAINT(self, self.Paint)
                except TypeError:
                    d = wx.MessageDialog(self, "No data to plot", "Error", wx.OK)
                    d.ShowModal()
                    d.Destroy()
                except ValueError:
                    d = wx.MessageDialog(self, "Unable to plot data", "Error", wx.OK)
                    d.ShowModal()
                    d.Destroy()
                except:
                    d = wx.MessageDialog(self, "An unknown error has occurred", "Error", wx.OK)
                    d.ShowModal()
                    d.Destroy()
            def Paint(self, e):
                dc = wx.PaintDC(self)
                dc.DrawBitmap(self.bitmap, 10, 40)
        
    class Form2(wx.SplitterWindow):
        appRef = None
        conFrame = {}
        def __init__(self, parent, id, appRef):
            wx.SplitterWindow.__init__(self,parent, -1, style=wx.SP_3D | wx.SP_BORDER)
            self.appRef = appRef
            self.classifierArray=[]
            sizer = wx.BoxSizer(wx.VERTICAL)
            self.panel_1 = wx.Panel(self, -1)
            self.testList = self._buildTestList()
            self.testSelection = wx.ComboBox(self.panel_1,30, choices= self.testList.keys())
            
            self.panel_2 = wx.Panel(self, -1)
            
            self.SplitHorizontally(self.panel_1,self.panel_2)
            wx.EVT_COMBOBOX(self.panel_1,30, self.buildTestPane)
        def buildTestPane(self,e):
            
            test = self.testList[self.testSelection.GetValue()]
            panelNew = wx.Panel(self, -1)
            horizBox = wx.BoxSizer(wx.HORIZONTAL)
            
            flexSizer = wx.FlexGridSizer(len(test.parameters.keys())+test.numClassifiers,2,9,25)
            
            addarray=[]
            self.classifierArray= [None]*test.numClassifiers
            for i in range(test.numClassifiers):
                self.classifList = self._buildClassifierList()
                self.classifierArray[i] = wx.ComboBox(panelNew,20+i, value=self.classifList.keys()[0],choices=self.classifList.keys())
                button = wx.Button(panelNew,40+i,"Configure",wx.Point(200,120))
                wx.EVT_BUTTON(self, 40+i, self._showConfigWindow)
                addarray.append((self.classifierArray[i], -1, wx.EXPAND))
                addarray.append((button, -1, wx.EXPAND))
            
            self.widgetlist = self._buildParamList(test.parameters,panelNew)
            flexSizer.AddMany(addarray+self.widgetlist)
                
                
            horizBox.Add(flexSizer, 1, wx.ALL | wx.EXPAND, 15)
            panelNew.SetSizer(horizBox)
            
            self.ReplaceWindow(self.panel_2,panelNew)
            self.panel_2 = panelNew
        def _buildClassifierList(self):
            self.appRef.classifierHash = {}
            self.appRef.classifierHash['Decision Tree']=DecTreeShim()
            self.appRef.classifierHash['SVM'] = SVMShim()
            self.appRef.classifierHash['AdaBoost M1']=AdaBoostShim()
            self.appRef.classifierHash['K Nearest Neighbor']=KNNShim()
            self.appRef.classifierHash['Tanh Neural Net']=TanhNNShim()
            self.appRef.classifierHash['Neural Net']=NNShim()
            self.appRef.classifierHash['Naive Bayes']=NBayesShim()
            self.appRef.classifierHash['SVM']=SVMShim()
            self.appRef.classifierHash['Bagging']=BaggingShim()
            return self.appRef.classifierHash
        
        def _buildTestList(self):
            self.appRef.testHash = {}
            self.appRef.testHash['K Fold'] = KFold()
            self.appRef.testHash['Plot Example'] = MatplotLibExample()
            self.appRef.testHash['Tournament'] = Tournament()
            return self.appRef.testHash
        
        def _showConfigWindow(self,e):
            print e.GetId()
            self.conFrame[e.GetId()] = self.configWindow(None,-1,"Classifier Parameter Configuration",self.appRef.classifierHash[self.classifierArray[e.GetId()-40].GetValue()],self.appRef,ident = e.GetId()-40)
        
        #fix
        
        def _buildParamList(self,parameters,panel):
            
            addArray = []
            for title, type in parameters.iteritems():
                #print title,type
                label,widget = self._buildWidget(title,type,panel)
                addArray.append((label, 1, wx.EXPAND))
                addArray.append((widget,1, wx.EXPAND))
            #print addArray
            return addArray
            
        
        def _buildWidget(self, title, typeTuple,panel):
            label = wx.StaticText(panel,-1,title+":")
            widget = None
            
            if typeTuple[1] == INTSELECTOR:
                widget = wx.SpinCtrl(panel,typeTuple[4],min=typeTuple[2],max=typeTuple[3],value = str(typeTuple[0]))
                wx.EVT_SPINCTRL(panel,typeTuple[4], self.configEvent)
            elif typeTuple[1] == FLOATSELECTOR:
                widget = wx.TextCtrl(panel,typeTuple[4], value = str(typeTuple[0]))
                
            return label,widget
        
        #end fix
        
        def configEvent(self,e):
            Test = self.appRef.form2.testList[self.appRef.form2.testSelection.GetValue()]
            #print Test
            ObjKey = None
            
            for key in Test.parameters.keys():
                if Test.parameters[key][4] == e.GetId():
                    ObjKey = key
                    break
            if Test.parameters[key][1] == INTSELECTOR:
                #print "int",e.GetInt()
                Test.setParameter(key,e.GetInt())
            elif Test.parameters[key][1] == FLOATSELECTOR:
                #print "float",float(e.GetString())
                Test.setParameter(key,float(e.GetString()))
            elif Test.parameters[key][1] == BOOLEAN:
                #print "bool",e.GetInt()
                Test.setParameter(key,e.GetInt())
            elif Test.parameters[key][1] == DROPSELECTOR:
                #print "string",e.GetString()
                Test.setParameter(key,e.GetString())
            
            #print e.GetId(), e.GetInt()
        
        class configWindow(wx.Dialog):
            Shim = None
            appRef = None
            paramClassifiers = {}
            clIndex = 0
            def __init__(self,parent,id,title,shim,appRef, ident = None):
                print shim,ident
                wx.Dialog.__init__(self,parent,wx.ID_ANY, title)
                self.appRef = appRef
                self.Shim = shim
                if ident != None: 
                    self.ident = ident
                else:
                    self.ident = 0
                horizBox = wx.BoxSizer(wx.HORIZONTAL)
                
                self.flexSizer = wx.FlexGridSizer(len(shim.parameters.keys()),2,9,25)
                
                okButton = wx.Button(self,1,'Ok')
                Nulllabel = wx.StaticText(self,-1,"") #this is a bad thing. must fix later
                
                widgetList = self._buildParamList(shim.parameters)
                widgetList.append((Nulllabel,1,wx.EXPAND))
                widgetList.append((okButton,1,wx.EXPAND))
                self.flexSizer.AddMany(widgetList)
                
                
                horizBox.Add(self.flexSizer, 1, wx.ALL | wx.EXPAND, 15)
                self.SetSizer(horizBox)
                
                wx.EVT_BUTTON(self,1,self.close)
                self.Fit()
                self.Centre()
                self.ShowModal()
                self.Destroy()
            def close(self,e):
                
                self.Close()
                
            def _buildParamList(self,parameters):
            
                addArray = []
                for title, type in parameters.iteritems():
                    #print title,type
                    label,widget = self._buildWidget(title,type)
                    addArray.append((label, 1, wx.EXPAND))
                    addArray.append((widget,1, wx.EXPAND))
                #print addArray
                return addArray
                
            
            def _buildWidget(self, title, typeTuple):
                
                label = None
                widget = None
                
                if typeTuple[1] == INTSELECTOR:
                    label = wx.StaticText(self,-1,title+":")
                    widget = wx.SpinCtrl(self,typeTuple[4],value = str(typeTuple[0]),min=typeTuple[2],max=typeTuple[3])
                    wx.EVT_SPINCTRL(self,typeTuple[4], self.configEvent)
                elif typeTuple[1] == FLOATSELECTOR:
                    label = wx.StaticText(self,-1,title+":")
                    widget = wx.TextCtrl(self,typeTuple[4],value= str(typeTuple[0]))
                    wx.EVT_TEXT(self,typeTuple[4], self.configEvent)
                elif typeTuple[1] == BOOLEAN:
                    label = wx.StaticText(self,-1,title+":")
                    widget = wx.CheckBox(self,typeTuple[4])
                    widget.SetValue(bool(typeTuple[0]))
                    wx.EVT_CHECKBOX(self,typeTuple[4], self.configEvent)
                elif typeTuple[1] == DROPSELECTOR:
                    label = wx.StaticText(self,-1,title+":")
                    widget = wx.ComboBox(self,typeTuple[4],value= typeTuple[0][0],choices=typeTuple[2])
                    wx.EVT_COMBOBOX(self,typeTuple[4], self.configEvent)
                elif typeTuple[1] == CLASSIFIERSELECTOR:
                    #need to overwrite widget
                    clist = self._buildClassifierList()
                    #widget = wx.ComboBox(self,typeTuple[4],choices=clist.keys(),value = clist.keys()[0])
                    widget = wx.ComboBox(self,typeTuple[4],choices=clist.keys(),value = clist.keys()[0])
                    label = wx.Button(self,8000,"Configure")
                    wx.EVT_BUTTON(self,8000, self.anotherWindow)
                    wx.EVT_COMBOBOX(self,typeTuple[4], self.configEvent)
                    self.paramClassifiers[typeTuple[4]] = clist
                elif typeTuple[1] == TEXT:
                    label = wx.StaticText(self,-1,title+":")
                    #fix
                    widget = wx.TextCtrl(self,typeTuple[4],value= str(typeTuple[0]))
                    wx.EVT_TEXT(self,typeTuple[4], self.configEvent)
                return label,widget
            def anotherWindow(self,e):
                Shim = self.appRef.form2.classifList[self.appRef.form2.classifierArray[0].GetValue()]
                ObjKey = None
                for key in Shim.parameters.keys():
                    if Shim.parameters[key][4] == e.GetId():
                        ObjKey = key
                        break
                param = self.paramClassifiers[Shim.parameters[key][4]]
                param = param[self.selclass]
                frame = self.appRef.form2.configWindow(None,-1,"Classifier Parameter Configuration",param,self.appRef)
                
            def configEvent(self,e):
                Shim = self.appRef.form2.classifList[self.appRef.form2.classifierArray[self.ident].GetValue()]
                #print Shim
                #print e.GetId(),
                #get object that has the id
                ObjKey = None
                for key in Shim.parameters.keys():
                    if Shim.parameters[key][4] == e.GetId():
                        ObjKey = key
                        break
                #what do we want to store?
                if Shim.parameters[key][1] == INTSELECTOR:
                    #print "int",e.GetInt()
                    Shim.setParameter(key,e.GetInt())
                elif Shim.parameters[key][1] == FLOATSELECTOR:
                    #print "float",float(e.GetString())
                    Shim.setParameter(key,float(e.GetString()))
                elif Shim.parameters[key][1] == BOOLEAN:
                    #print "bool",e.GetInt()
                    Shim.setParameter(key,e.GetInt())
                elif Shim.parameters[key][1] == DROPSELECTOR:
                    #print "string",e.GetString()
                    Shim.setParameter(key,e.GetString())
                elif Shim.parameters[key][1] == CLASSIFIERSELECTOR:
                    # selected classifier 
                    self.selclass = e.GetString()
                    param = self.paramClassifiers[Shim.parameters[key][4]]
                    Shim.setParameter(key,param)
                
                #print e.GetId(),e.GetString(),e.GetEventObject(),e.GetEventType()
            def _buildClassifierList(self):
                classifierHash = {}
                classifierHash['Decision Tree']=DecTreeShim()
                classifierHash['SVM'] = SVMShim()
                classifierHash['AdaBoost M1']=AdaBoostShim()
                classifierHash['K Nearest Neighbor']=KNNShim()
                classifierHash['Tanh Neural Net']=TanhNNShim()
                classifierHash['Neural Net']=NNShim()
                classifierHash['Naive Bayes']=NBayesShim()
                classifierHash['SVM']=SVMShim()
                classifierHash['Bagging']=BaggingShim()
                classifierHash['None']=EmptyShim()
                return classifierHash
    class Form3(wx.Panel):
        def __init__(self, parent, id, appRef):
            wx.Panel.__init__(self, parent, id)
            
            self.runButton = wx.Button(self, 101, "Run" , wx.Point(10,10))
            self.saveButton = wx.Button(self, 102, "Save Model", wx.Point(150,10))
            self.stat = wx.TextCtrl(self,-1, "", wx.Point(50,100), wx.Size(400,300), wx.TE_MULTILINE | wx.TE_READONLY)
            #self.plotButton.Enable(False)
            
            wx.EVT_BUTTON(self, 101, self.runTest)
            wx.EVT_BUTTON(self, 102, self.saveDialog)
            self.appRef = appRef
        def saveDialog(self,e):
            saver = wx.FileDialog(self, "Save model", ".", "model", "*.pickle", wx.SAVE)
            saver.ShowModal()
            #fix for many classifiers
            #try:
            name = saver.GetFilename()
            splitname = os.path.splitext(name)
            if splitname[1] != ".pickle":
                name = splitname[0]+".pickle"
            cl = self.appRef.classifierHash[self.appRef.form2.classifierArray[0].GetValue()]
            directory = os.path.join(saver.GetDirectory(),name)
            print directory
            cl.writeToFile(directory)
            #except:
                #d = wx.MessageDialog(self, "Unable to save model", "Error", wx.OK)
                #d.ShowModal()
                #d.Destroy()
            saver.Destroy()
            
        def runTest(self, e):
            self.stat.Clear()
            self.stat.AppendText("Working...")
            test = self.appRef.testHash[self.appRef.form2.testSelection.GetValue()]
            clList = [None]*test.numClassifiers
            for i in range(test.numClassifiers):
                cl = self.appRef.classifierHash[self.appRef.form2.classifierArray[i].GetValue()]
                cl.construct()
                #print cl
                clList[i] = cl.get()
            test.run(clList, self.appRef.trainingSet, self.appRef.classifierHash[self.appRef.form2.classifierArray[0].GetValue()].parameters)
            
            self.Refresh()
            self.stat.AppendText("Done\n")
            #get results and display them 
            
            
            if test.resultType == ENUM:
                for item, result in test.results.iteritems():
                    self.stat.AppendText(item+": "+str(result)+"\n")
            elif test.resultType == GRAPH:
                pframe = self.graphWindow()
                #self.bitmap = wx.Bitmap("fig.jpg")
                #wx.EVT_PAINT(self, self.Paint)
                #self.Refresh()
                #self.plotButton.Enable(True)
                #do graphing
            
            #for item, result in test.results.iteritems():
                #print item, result
        class graphWindow(wx.Frame):
            def __init__(self):
                wx.Frame.__init__(self,None,wx.ID_ANY, "Plot", size=(750,750))
                self.bitmap = wx.Bitmap("fig.jpg")
                wx.EVT_PAINT(self, self.Paint)
                self.Show(True)
        

            def Paint(self, e):
                dc = wx.PaintDC(self)
                dc.DrawBitmap(self.bitmap, 10, 40)

#types for config
BOOLEAN = 1 # (var, type, default)
INTSELECTOR = 2
FLOATSELECTOR = 3
DROPSELECTOR = 4 # (var, type, list of vals, list of nums)
CLASSIFIERSELECTOR = 5
TEXT = 6
# (var, type, lowerbound, upper)

#types for results
NONE = 0
ENUM = 1
GRAPH = 2

            
if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = VisualClassifier(None,-1, "ML1050 Visual Classifier")
    app.MainLoop()
