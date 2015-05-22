#!/usr/bin/env python
# file: test_unittests.py

"""A centralized place to test all tests."""

import unittest
import doctest

# These are modules with doctests.  Import them and put them in the
# tuple below.
import Example, TrainingSet
import Preprocessing.CrossValidation, Preprocessing.Bootstrapping
import Classifiers.kNN, Classifiers.DecisionTree
modules = (Example,
           TrainingSet,
           Preprocessing.CrossValidation,
           Preprocessing.Bootstrapping,
           Classifiers.kNN,
           Classifiers.DecisionTree,
           )

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    # Create a TestSuite from the doctests in the first module
    fullSuite = doctest.DocTestSuite(modules[0])
    # Grow the TestSuite with the doctests in the other modules
    for mod in modules:
        # Cheating a bit by using the private _tests list, but there
        # is no other way to get the tests from a suite.
        fullSuite.addTests(doctest.DocTestSuite(mod)._tests)
    runner.run(fullSuite)

    # Another way that doesn't cheat but creates multiple suites.  I
    # don't like this because it doesn't summarize the results
#     for mod in modules:
#         suite = doctest.DocTestSuite(mod)
#         runner.run(suite)
