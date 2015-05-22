'''
Simple Bayesian Network classifier.
The examples and documentation rely heavily on Duda's 'Belief Network for Fish'
in chapter 2.

The primary goal of this module is to allow the evaluation of 
expressions in the form
  P(q|a1,b2,v,c3)
The result are the values of 'q' for all values of 'v'.  Assumming that the
data may be expressed with each variable (x) assumming a finite number of
distinct values (1,2,3,...x_n) eases the implementation of parsing and
evaluating the above expression.  It seems trivial to write wrappers that
convert
  P(thin|north_atlantic,winter,fish)
into the appropriate
  P(d|b1,a1,x)
form for this module.
  
'''


def ParsePBar( text_expr) :
    '''A simple routine to parse an initial expression in the form
      P(q|aI,bJ,c,dK)
    into a left side
      left = 'q'
      right = [ 'aI', 'bJ', 'c', 'dK' ]

    >>> ParsePBar( 'P(q|a1,b2,c,d3)' )
    ('q', ['a1', 'b2', 'c', 'd3'])
    '''
    inside = text_expr.split("(")[1]
    inside = inside.split(")")[0]
    bar = inside.split("|")

    left = bar[0]
    rlist= bar[1].split(",")
    return left, rlist

class BeliefNetwork( dict ) :
    class Node( object ) :
        '''Object representing one node in a belief net.'''
        def __init__( self, name, iter_vals_seq, var_order_seq, ptable ) :
            '''name = the name of the table, ONLY THE FIRST CHARACTER OF THE NAME IS 
               REGISTERED!  For instance:  'a', or 'a_season'
            iter_vals_seq = a sequence of numbers representing the index values
               this variable may attain.  For instance (1,2,3,4) for
               ("winter","spring","summer","autumn").
            var_order_seq = a sequence of names representing the tuple-key order in
               which values are encoded within ptable.  For instance ("x","a","b") or
               ("x_fish","a_season","b_locale") for the 'fish' node in the Duda example.
               The above is interpretted as:
                 ptable[(1,1,2)] = 0.7
                 ptable[(2,3,2)] = 0.9
               If var_order_seq is None, then this node represents a simple prior node
               in which case the keys SHOULD NOT be tuples.  For instance, the 
               "b_locale", ptable = { 1:0.6, 2:0.4 } 
            ptable = a dictionary mapping integer-tuple-keys to probabilities.  See the 
               above comment on var_order_seq.
            '''
            self.name = name
            # we only use one character names internally
            self.__rn = name[0]
            # ie: (1,2,3) or ("summer", "winter", ... )
            self.iv = tuple( iter_vals_seq)
            # the order of expression names in the ptable tuple key
            # if None, they my table has one lookup and it is my name value
            self.tp = None
            if var_order_seq is not None :
                self.tp = tuple( var_order_seq )
            # you guessed it, the Ptable for this node
            self.ptable = ptable

        def iterate_expr( self, input_expression={} ) :
            '''Inspect the input_expression for my term.  If it is missing,
            return a tuple of input_expressions augmented by each of my index values.
            If my variable term already exists in input_expression, simply return
            the expression in a 1-len tuple.

            This is the marginalzation step in the calculation.
            '''
            input_expression.setdefault(self.__rn, None)
            myval = input_expression[self.__rn]
            if myval is not None :
                # then fling the expression back
                return (input_expression,)

            # otherwise, return a tuple of expressions with all of
            # my values
            l = []
            for i in self.iv :
                d = {}
                d.update( input_expression )
                d[self.__rn] = i
                l.append(d)
            
            return tuple(l)

        def value( self, fixed_expr ) :
            '''Return my table entry for any of the fixed_expr entries 
            I am responsible for.'''
            k = None
            if self.tp is None :
                # I am a prior table, just my own name key
                # NOT A TUPLE KEY
                k = fixed_expr[self.__rn]
            else :
                # otherwise, build a key sequence
                l = []
                for n in self.tp :
                    l.append( fixed_expr[n] )

                k = tuple(l)

            if not self.ptable.has_key(k) :
                RuntimeError( (self.__rn,k,self.ptable) )

            # and use it
            v = self.ptable[k]
            #print self.name, k, v
            return self.ptable[k]

    '''The primary object for evaluating simple bayesian networks.

    Internally, a BeliefNetwork communicates to its Nodes through
    'expressions'.  Expressions are simply dictionaries with 1-character name
    keys and integer values.  For instance, there is an expression inside of 
    the conditional probability:
      P(q|aI,bJ,c,dK)
    it is
      { 'a':I, 'b':J, 'd':K }
    Note that the 'c' entry is missing, and the engine will fill its values 
    via the 'c' Node's .iterate_expr() method.
    '''
    def __init__( self, *bayes_nodes ) :
        dict.__init__( self )
        for bn in bayes_nodes :
            self.add( bn )

    def __call__( self, pbar_expr ) :
        '''Wrapper for self.eval( pbar_expr ).'''
        return self.eval( pbar_expr )

    def __register_node( self, bn ) :
        # registers a node with the first character of its name
        self[bn.name[0]] = bn

    def __value_expr( self, expr ) :
        '''Return a final value for expression.  For the input expression expr,
        marginalize over all unknown variables and return a value.'''
        r = 0.0
        stack=[expr]
        while len(stack) :
            e = stack[-1]
            stack = stack[:-1]

            process = True
            for name in self.keys() :
                if not e.has_key( name ) or ( e[name] is None ):
                    iterated_over = self[name].iterate_expr( e )
                    if len( iterated_over ) > 1 :
                        # back to the stack
                        stack.extend( iterated_over )
                        # and start over
                        process = False
                        break;

            if process :
                # okay we have a full fledged expression, find the product
                # and lump onto the sum
                p = 1
                for node in self.values() :
                    p *= node.value( e )
                r += p

        return r


    def add( self, *args ) :
        '''Add BeliefNetwork.Nodes.  args may be a list of pre-existing
        nodes, or a series of
          name, iter_vals_tuple, tuplekey, ptable
        variables used for creating one.
        '''
        while len( args ) :
            if isinstance( args[0], ( BeliefNetwork.Node, )) :
                self.__register_node( args[0] ) 
                # 'shift'
                args = args[1:]
            else :
                # assume 4 arguments
                self.__register_node( BeliefNetwork.Node( *args[0:4] ))
                # 'shift'
                args = args[4:]

    def eval( self, pbar_expr, write_file=None ) :
        '''Evaluates pbar_expr.  Given
          P(q|aI,bJ,c,dK) where q in {q1, q2, q3},
        returns a list of tuples:
          [ ('q1', P(q1|aI,bJ,c,dK) ), ('q2', P(q2|aI,bJ,c,dK ),  ('q3', P(q2|aI,bJ,c,dK ) ]
        Note that the first term is a string, not an integer.

        If write_file is not None, then verbose calculation results are printed via its
        .write() method.
        
        NOTE:  this document shows Duda's 'Belief Network for Fish' in action. There appears
        to be erroneous calculations in the book examples:
        - On pages 58,59 the book uses P(x_2|a_3,b_1) as 0.4 when it is actually 0.6.  The value
          for P(a_3,b_1,x_2,c_3,d_2) is actually 0.26...
        - On page 61, the cited solution of P(x_2|c_1,b_2) = alpha*0.066 should actually be 
          alpha*0.042.

        >>> apriors = {1:0.25, 2:0.25, 3:0.25, 4:0.25}
        >>> bpriors = {1:0.6, 2:0.4}
        >>> # xi, ai, bi
        >>> xtable = { (1,1,1):0.5, (2,1,1):0.5, (1,1,2):0.7, (2,1,2):.3, (1,2,1):0.6, (2,2,1):.4, (1,2,2):.8, (2,2,2):.2, (1,3,1):0.4, (2,3,1):.6, (1,3,2):.1, (2,3,2):.9, (1,4,1):0.2, (2,4,1):.8, (1,4,2):.3, (2,4,2):.7 }
        >>> # ci, xi
        >>> ctable = { (1,1):0.6, (2,1):0.2, (3,1):0.2, (1,2):0.2, (2,2):0.3, (3,2):0.5 }
        >>> # di, xi
        >>> dtable = { (1,1):0.3, (2,1):0.7, (1,2):0.6, (2,2):0.4 }
        >>> bnet = BeliefNetwork( BeliefNetwork.Node( "a", (1,2,3,4), None, apriors ))
        >>> bnet.add( BeliefNetwork.Node( "b", (1,2), None, bpriors )) 
        >>> bnet.add( "x", (1,2), ("x","a","b"), xtable )
        >>> bnet.add( "c", (1,2,3), ("c","x"), ctable, "d", (1,2), ("d","x"), dtable )
        >>> bnet.eval( 'P(a|b1,x2,c3,d2)' )
        [('a1', 0.21739130434782605), ('a2', 0.17391304347826086), ('a3', 0.26086956521739124), ('a4', 0.34782608695652173)]
        >>> bnet.eval( 'P(x|c1,b2' )
        [('x1', 0.73076923076923084), ('x2', 0.26923076923076927)]
        >>> print "Duda page 60-61 P(x_2|c_1,b_2) =", "%.3f" % bnet.eval( 'P(x|c1,b2' )[1][1]
        Duda page 60-61 P(x_2|c_1,b_2) = 0.269
        '''
        # parse the expression
        left, rlist = ParsePBar( pbar_expr )
       
        # the query variable
        q = left[0]

        # retrieve the class instance for the q-node
        q_class_instance = eval( q, globals(), self )
        # retrieve the full fledged baysian expression for each index of 
        # the query variable
        q_iter_expressions = q_class_instance.iterate_expr()

        # okay, for each variable in the rlist, we only deal with it if it is formatted
        # as <v><i> (two characters).  this means that particular variable won't
        # be marginalized over in the calculations, and we can simple grab a reference
        # to the probability that will be used in the calculations (that 'reference', it
        # the index!)
        for vi in rlist :
            if len(vi) == 2 :
                for qi in q_iter_expressions :
                    qi[vi[0]] = int(vi[1])

        # now the only variables missing in qi are the ones we are going to marginalize over
        # ...so lets do it
        qvalues = {}
        for qi in q_iter_expressions :
            qvalues[qi[q]] = self.__value_expr( qi )

        # sum up for normalization
        n = sum( qvalues.values() )
        
        r = []
        for k, v in qvalues.items() :
            normalized = v/n
            r.append( (q+str(k),normalized) )
            if write_file :
                write_file.write( "P(%s%d|%s) = %.5f/%.5f = %.5f\n" % (q, k, ",".join(rlist), v, n, v/n) )

        return r

def _test():
    """Run the tests in the documentation strings."""
    import doctest
    return doctest.testmod(verbose=True)
    
if __name__ == "__main__":
    try:
        __IP                            # Are we running IPython?
    except NameError:
        _test()                         # If not, run the tests


