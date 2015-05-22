'''A module providing simple statistical measures.
'''

import math


class BaseStats( object ) :
	'''A base class for stat-tracking objects.
	
	PROPERTIES:
	 n, mean = the obvious inteprettation 
	 varn, sdn = the MLE estimation of variance and standard deviation
	 vars, sds = the unbiased estimation of variance and standard deviation
	'''
	n = property( lambda s : s._n )
	mean = property( lambda s : s._m )
	varn = property( lambda s : s.get_mlevar() )
	vars = property( lambda s : s.get_vars() )
	sdn = property( lambda s : math.sqrt(s.varn) )
	sds = property( lambda s : math.sqrt(s.vars) )

        this_is_a_new_var = 1

	def __init__( self ) :
		self.clear()

	def clear( self ) :
		'''Forget all data.  Reinitializes the object.'''
		self._n = 0.0
		self._m = 0.0
		self._vn = 0.0

	def get_mlevar( self ) :
		'''Return the current MLE variance or zero if there are insufficient
		datapoints.
		'''
		if self._n :
			return self._vn / self._n
		return 0.0

	def get_vars( self ) :
		'''Return the unbiased sample variance or zero if there are insufficient
		datapoints.
		'''
		if self._n > 1 :
			return self._vn / (self._n-1)
		return 0.0

	def __call__( self, *args ) :
		'''Return the mean after incorporating any args datapoints.'''
		for a in args :
			self.add(a)

		return self.mean

	def __len__( self ) :
		'''Return self.n'''
		return self.n

	def __norm( self, x, sd ) :
		'''Return the normalized (z-statisitc) for x against the mean and 
		provided measure of spread.
		'''
		if sd <= 0.0 :
			return x-self.mean
		return (x-self.mean)/sd

	def normn( self, x ) :
		'''Return a normalized statistic for x based on the variance MLE.'''
		return self.__norm(x,self.sdn)

	def norms( self, x ) :
		'''Return a normalized statistic for x based on unbiased variance.'''
		return self.__norm(x,self.sds)

	def add( self, a ) :
		'''Must be implemented by a subclass.  Add the data point a to the object.
		'''
		raise NotImplementedError()


class RunningStats( BaseStats ) :
	'''Welford's One-Pass Algorithm for mean and variance.  Ripped ungraciously
	from the pages of *Discrete Event Simulation, A First Course* by Leemis and
	Park.

	The advantange of this algorithm is that the data does not have to be retained.

	PROPERTIES (in addition to BaseStats)
	  min, max, sum, product =  the obvious inteprettation 

	>>> rs = RunningStats( [ 1,2,3,4,5 ] )
	>>> print rs.n, rs.mean, rs.varn, rs.sds
	5.0 3.0 2.0 1.58113883008
	>>> rs.add(10)
	>>> print rs.n, rs.mean, rs.varn, rs.sds
	6.0 4.16666666667 8.47222222222 3.18852107828
	>>> rs( 20, 30, 40 )
	12.777777777777779
	>>> print rs.n, rs.mean, rs.varn, rs.sds
	9.0 12.7777777778 176.172839506 14.0781548665
	>>> len(rs)
	9
	>>> rs.clear()
	>>> len(rs)
	0
	>>> rs.add(1)
	>>> print rs.n, rs.mean, rs.varn, rs.sds
	1.0 1.0 0.0 0.0
	>>> 
	'''
	min = property( lambda s : float(s.__min) )
	max = property( lambda s : float(s.__max) )
	sum = property( lambda s : s.__sum )
	product = property( lambda s : s.__prod )

	def __init__( self, initdata=[] ) :
		'''initdata should be a list of data points'''
		BaseStats.__init__( self )
		self.clear()
		map( self, initdata )

	def clear( self ) :
		self.__min = None
		self.__max = None
		self.__sum = 0.0
		self.__prod = 1.0
		BaseStats.clear( self )

	def add( self, a ) :
		self._n, self.__min, self.__max, self.__sum, self.__prod, self._m, self._vn = self.whatif(a)

	def whatif( self, number ) :
		'''Return the n, min, max, sum, product, mean, varn if number is added
		to running calculations.
		'''
		newn = self._n + 1
		# tmp
		d = float(number) - self._m
		# update var
		newvn = self._vn + (float(self._n)/float(newn))*(d)**2
		# update mean
		newmean = self._m + (d/newn)
		# update min	
		newmin = number
		if self.__min is not None :
			newmin = min( newmin, self.__min )
		# update max	
		newmax = number
		if self.__max is not None :
			newmax = max( newmax, self.__max )
		# update sum and product
		newsum = self.__sum + number
		newprod = self.__prod * number

		return (newn, newmin, newmax, newsum, newprod, newmean, newvn )


if __name__ == '__main__' :
	if False :
		print "== AVERAGE TEST =="
		lf = 0.1
		wma = WeightedMovingAverage( lf )
		print "0.1 wma", "pre:", wma, "post + 1", wma.add( 1 )(), lf*(1) 
		print "0.1 wma", "pre:", wma, "post + 5", wma.add( 5 )(), lf*5 + lf*(1)*(1-lf)

		lf = 0.9
		dra = DecayedRunningAverage( lf, 3, 2 )
		print "0.9, 3, 2 dra", repr(dra)
		dra.add(4)
		print "0.9, 3, 2 dra post add 4", repr(dra)
		dra.add(6)
		print "0.9, 3, 2 dra post add 6", repr(dra)


	if True :
		# These are stupid implementations for mean and variance MLEs, note the 
		# lack of error checking on len(iterable)
		def __mean( iterable ) :
			x = 0.0
			for i in iterable :
				x += i
			return x / len(iterable)

		def __var( mean, iterable ) :
			x = 0.0
			for i in iterable :
				x += ( i - mean )**2
			return x / len(iterable)
		
		print "== WELFORD TEST =="
		print RunningStats( [0,1,0,1] )()
		import random
		u = []; v=[]
		ru = RunningStats()
		rv = RunningStats()
		for x in xrange(10) :
			u.append( random.gauss( 3, 3 ))
			v.append( random.gauss( 3, 3 ))

			# must do one-pass covariance *first*, then add datapoints to running means
			ru( u[-1] )
			rv( v[-1] )

		mu=__mean(u)
		mv=__mean(v)
		vu=__var(mu,u)
		vv=__var(mv,v)

		print "var u:", len(ru), min(u), max(u), mu, vu, "running:", ru() 
		print "var v:", len(rv), min(v), max(v), mv, vv, "running:", rv() 


def _test():
    """Run the tests in the documentation strings."""
    import doctest
    return doctest.testmod(verbose=True)
    
if __name__ == "__main__":
    try:
        __IP                            # Are we running IPython?
    except NameError:
        _test()                         # If not, run the tests

