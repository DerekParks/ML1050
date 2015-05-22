import random
"""A set of functions reinventing the wheel, why?  because in this case it
   was faster than figuring out how to do it properly.  The real goal is
   to provide the create2DNormalLinearCorrelatedData function

   >>>import Utils.CovariantDataGenerator
   >>>mydata = create2DNormalLinearCorrelatedData(1,1,3,3,1,200)
   >>>myxs = mydata[0]
   >>>myys = mydata[1]
   
   >>>for item in range(1,len(myxs)):
   >>>  print str(myxs[item])+","+str(myys[item])
   

   Note I have not put what the output is as it should be random! 

   You can also declare a function of y=g(x) in order to get a different distrib   ution of data.  To do so, declare a function that returns a value given a par   ameter:

   >>>def testFunction(x):
   >>>  return x*x

   Now pass that into the create2DNormalCorrelatedData function, with xmean, xstddev, ystddev, and number of points:

   >>>mydata = create2DNormalCorrelatedData(testFunction,0,4,.5,100)

   Again the result will be a list containing a list of x values and y values

   >>>myxs = mydata[0]
   >>>myys = mydata[1]

"""

def uniform(theta):
  """A function that returns a sample from a Uniform(0,theta)"""
  return theta*random.random()

def pseudoNormal(mean, stdDeviation):
  """A pseudoNormal sample, old school style as the mean of 12 uniform samples"""
  sum = 0
  number = 12
  for i in range(1,number+1):
    sum = sum + (mean - stdDeviation*(.5) + stdDeviation*uniform(1))

  return sum / number

def create2DNormalCorrelatedData(fx,xmean,xstddev,ystddev,numberpoints):
  """Creates a 2 dimensional correlated gaussian fuzz around the function
   of fx near the point xmean.

   Returns a list containing two lists: one of x coordinates, one of y coordinates
  """
  xvalues = []
  yvalues = []
  for i in range(1,numberpoints+1):
    x = pseudoNormal(xmean,xstddev) #Get a pseudoNormal x near xmean
    y = fx(x)+pseudoNormal(0,ystddev) #Get a corresponding y value near g(x)
    xvalues.append(x)
    yvalues.append(y)

  result = []
  result.append(xvalues)
  result.append(yvalues)
  return result




def create2DNormalLinearCorrelatedData(a, b, xmean, xstddev, ystddev, numberpoints):
  """Creates 2 dimensions of linearlly correlated data with a normal deviation
   in both x and y directions.  The form of this is that you want them both in
   a line of the nature aX + b, but then with fuzz off of that.

   Returns a list containing two lists: one of x coordinates, and one of y coordinates.
  """
  xvalues = []
  yvalues = []
  for i in range(1,numberpoints+1):
    x = pseudoNormal(xmean,xstddev) #Get a pseudoNormal x near xmean
    y = a*x+b+pseudoNormal(0,ystddev) #Get a corresponding y value near g(x)
    xvalues.append(x)
    yvalues.append(y)

  result = []
  result.append(xvalues)
  result.append(yvalues)
  return result

"""
#Generation of SkiTracks dataset.
def testFunction(x):
   return x*x
def otherFunction(x):
   return x*x+2
mydata = create2DNormalCorrelatedData(testFunction,0,10,1,200)
myxs = mydata[0]
myys = mydata[1]
for i in range(len(myxs)):
  print "1,"+str(myxs[i])+","+str(myys[i])

mydata = create2DNormalCorrelatedData(otherFunction,-.5,6,1,200)
myxs = mydata[0]
myys = mydata[1]
for i in range(len(myxs)):
  print "0,"+str(myxs[i])+","+str(myys[i])
"""
