#! /usr/bin/env python
text = '''
<SOAP-ENV:Envelope xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/"
    xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:xsi="http://www.w3.org/1999/XMLSchema-instance"
    xmlns:xsd="http://www.w3.org/1999/XMLSchema"
    xmlns:xmlsoap="http://xml.apache.org/xml-soap">
<SOAP-ENV:Body>
<c-gensym1 xsi:type="xmlsoap:Map">
  <item>
    <key xsi:type="SOAP-ENC:base64">AAE=</key>
    <value xsi:type="xsd:int">456</value>
  </item>
  <item>
    <key xsi:type="xsd:string">a</key>
    <value xsi:type="xsd:int">123</value>
  </item>
</c-gensym1>
</SOAP-ENV:Body>
</SOAP-ENV:Envelope>
'''

from ZSI import *
from ZSI import *
ps = ParsedSoap(text)

tcdict = TC.Apache.Map()
tclist = TC.Apache.Map(aslist=1)

d = tcdict.parse(ps.body_root, ps)
print 'as dictionary\n', d
l = tclist.parse(ps.body_root, ps)
print '\n', '=' * 30
print 'as list\n', l


import sys

print '\n', '=' * 30
sw = SoapWriter(sys.stdout)
tcdict.serialize(sw, d)
sw.close()

print '\n', '=' * 30
sw = SoapWriter(sys.stdout)
tclist.serialize(sw, l)
sw.close()
