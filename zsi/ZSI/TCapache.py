#! /usr/bin/env python
# $Header$
'''Apache typecodes.
'''

from ZSI import _copyright, _child_elements
from ZSI.TC import TypeCode, Struct as _Struct, Any as _Any

class Apache:
    NS = "http://xml.apache.org/xml-soap"

class _Map(TypeCode):
    '''Apache's "Map" type.
    '''
    parselist = [ (Apache.NS, 'Map') ]

    def __init__(self, pname=None, **kw):
	TypeCode.__init__(self, pname, **kw)
	self.aslist = kw.get('aslist', 0)
	self.tc = _Struct(None, [ _Any('key'), _Any('value') ], inline=1)

    def parse(self, elt, ps):
	self.checkname(elt, ps)
	if self.nilled(elt, ps): return None
	p = self.tc.parse
	if self.aslist:
	    v = []
	    for c in _child_elements(elt):
		d = p(c, ps)
		v.append((d['key'], d['value']))
	else:
	    v = {}
	    for c in _child_elements(elt):
		d = p(c, ps)
		v[d['key']] = d['value']
	return v

    def serialize(self, sw, pyobj, **kw):
	n = kw.get('name', self.oname) or 'E%x' % id(pyobj)
	if self.typed:
	    tstr = ' A:Map xmlns:A="%s"' % Apache.NS
	else:
	    tstr = ''
	print >>sw, "<%s%s%s>" % (n, kw.get('attrtext', ''), tstr)
	if self.aslist:
	    for k,v in pyobj:
		self.tc.serialize(sw, {'key': k, 'value': v}, name='item')
	else:
	    for k,v in pyobj.items():
		self.tc.serialize(sw, {'key': k, 'value': v}, name='item')
	print >>sw, "</%s>" % n


class _SOAPStruct(TypeCode):
    '''Apache's "SOAPStruct" type.
    '''
    parselist = [ (Apache.NS, 'SOAPStruct') ]

    def __init__(self, pname=None, **kw):
	TypeCode.__init__(self, pname, **kw)
	self.aslist = kw.get('aslist', 0)
	self.tc = _Any(optional=1)

    def parse(self, elt, ps):
	self.checkname(elt, ps)
	if self.nilled(elt, ps): return None
	p = self.tc.parse
	if self.aslist:
	    v = [ p(c, ps) for c in _child_elements(elt) ]
	else:
	    v = {}
	    for c in _child_elements(elt):
		v[c.localName] = p(c, ps)
	return v


Apache.Map = _Map
Apache.SOAPStruct = _SOAPStruct

if __name__ == '__main__': print _copyright