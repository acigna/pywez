#!/usr/bin/env python
############################################################################
# Joshua R. Boverhof, LBNL
# See Copyright for copyright notice!
###########################################################################
import sys, unittest
from ConfigParser import ConfigParser, NoOptionError
from ServiceTest import CONFIG_PARSER, DOCUMENT, LITERAL, BROKE, TESTS

def makeTestSuite(document=None, literal=None, broke=None):
    """Return a test suite containing all test cases that satisfy 
       the parameters. None means don't check.

       document -- None, True, False
       literal -- None, True, False
       broke -- None, True, False
    """
    cp = CONFIG_PARSER
    testSections = []
    for section in cp.sections():
        try:
            if (document is not None) and (cp.getboolean(section, DOCUMENT) is not document):
                pass
            elif (literal is not None) and (cp.getboolean(section, LITERAL) is not literal):
                pass
            elif (broke is not None) and (cp.getboolean(section, BROKE) is not broke):
                pass
            else:
                testSections.append(section)
        except NoOptionError, ex: 
            pass
    suite = unittest.TestSuite()
    for section in testSections:
        moduleList = cp.get(section, TESTS).split()
        for module in  map(__import__, moduleList):
            s = module.makeTestSuite()
            s.setSection(section)
            suite.addTest(s)
    return suite

def brokeTestSuite():
    return makeTestSuite(broke=True)

def workingTestSuite():
    return makeTestSuite(broke=False)

def docLitTestSuite():
    return makeTestSuite(document=True, literal=True)

def main():
    """Gets tests to run from configuration file.
    """
    unittest.TestProgram(defaultTest="brokeTestSuite")

if __name__ == "__main__" : main()
    
