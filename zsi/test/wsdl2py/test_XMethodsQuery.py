#!/usr/bin/env python

############################################################################
# David W. Robertson, LBNL
# See LBNLCopyright for copyright notice!
###########################################################################
import sys, unittest
from ZSI import EvaluateException

import utils
from paramWrapper import ResultsToStr

"""
Unittest for contacting the XMethodsQuery Web service.

WSDL:  http://www.xmethods.net/wsdl/query.wsdl
"""


class XMethodsQueryTest(unittest.TestCase):
    """Test case for XMethodsQuery Web service
    """

    def test_getAllServiceNames(self):
        request = portType.inputWrapper('getAllServiceNames')
        response = portType.getAllServiceNames(request)   
        print ResultsToStr(response)

    def test_getAllServiceSummaries(self):
        request = portType.inputWrapper('getAllServiceSummaries')
        response = portType.getAllServiceSummaries(request)   
        print ResultsToStr(response)

    def test_getServiceDetail(self):
        request = portType.inputWrapper('getServiceDetail')
        request._id = 'uuid:A29C0D6C-5529-0D27-A91A-8E02D343532B'
        response = portType.getServiceDetail(request)   
        print ResultsToStr(response)
    
    def test_getServiceNamesByPublisher(self):
        request = portType.inputWrapper('getServiceNamesByPublisher')
        request._publisherID = 'xmethods.net'
        response = portType.getServiceNamesByPublisher(request)   
        print ResultsToStr(response)
    
    def test_getServiceSummariesByPublisher(self):
        request = portType.inputWrapper('getServiceSummariesByPublisher')
        request._publisherID = 'xmethods.net'
        response = portType.getServiceSummariesByPublisher(request)   
        print ResultsToStr(response)


def makeTestSuite():
    global service, portType

    kw = {}
    setUp = utils.TestSetUp('config.txt')
    serviceLoc = setUp.get('complex_types', 'XMethodsQuery')
    useTracefile = setUp.get('configuration', 'tracefile') 
    if useTracefile == '1':
        kw['tracefile'] = sys.stdout
    service, portType = setUp.setService(XMethodsQueryTest, serviceLoc,
                                'XMethodsQuery', 'XMethodsQuerySoapPortType',
                                **kw)

    suite = unittest.TestSuite()
    if service:
        suite.addTest(unittest.makeSuite(XMethodsQueryTest, 'test_'))
    return suite


if __name__ == "__main__" :
    utils.TestProgram(defaultTest="makeTestSuite")
