#!/usr/bin/env python

# Copyright (c) 2001 actzero, inc. All rights reserved.

import sys

sys.path.insert (1, '..')

import SOAP

ident = '$Id$'

SoapEndpointURL		= 'http://www.alanbushtrust.org.uk/soap/compositions.asp'
MethodNamespaceURI 	= 'urn:alanbushtrust-org-uk:soap:methods'
SoapAction		= MethodNamespaceURI + "#GetCategories"

server = SOAP.SOAPProxy( SoapEndpointURL, namespace=MethodNamespaceURI, soapaction=SoapAction )
print "server level>>", server.GetCategories()
