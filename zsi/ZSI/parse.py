#! /usr/bin/env python
# $Header$
'''SOAP messaging parsing.
'''

from ZSI import _copyright, _children, _attrs, _child_elements, _stringtypes, \
        _backtrace, EvaluateException, ParseException, _valid_encoding, \
        _Node, _find_attr
import types
try:
    from xml.ns import SOAP, XMLNS
except:
    from ZSI.compat import SOAP, XMLNS

_find_actor = lambda E: E.getAttributeNS(SOAP.ENV, "actor") or None
_find_mu = lambda E: E.getAttributeNS(SOAP.ENV, "mustUnderstand")
_find_root = lambda E: E.getAttributeNS(SOAP.ENC, "root")
_find_id = lambda E: _find_attr(E, 'id')

class ParsedSoap:
    '''A Parsed SOAP object.
        Convert the text to a DOM tree and parse SOAP elements.
        Instance data:
            reader -- the DOM reader
            dom -- the DOM object
            ns_cache -- dictionary (by id(node)) of namespace dictionaries
            id_cache -- dictionary (by XML ID attr) of elements
            envelope -- the node holding the SOAP Envelope
            header -- the node holding the SOAP Header (or None)
            body -- the node holding the SOAP Body
            body_root -- the serialization root in the SOAP Body
            data_elements -- list of non-root elements in the SOAP Body
            trailer_elements -- list of elements following the SOAP body
    '''

    def __init__(self, input, **kw):
        '''Initialize.
        Keyword arguments:
            trailers -- allow trailer elments (default is zero)
            resolver -- function (bound method) to resolve URI's
            readerclass -- factory class to create a reader
            keepdom -- do not release the DOM
        '''

        self.readerclass = kw.get('readerclass')
        if not self.readerclass:
            from xml.dom.ext.reader import PyExpat
            self.readerclass = PyExpat.Reader
        try:
            self.reader = self.readerclass()
            if type(input) in _stringtypes:
                self.dom = self.reader.fromString(input)
            else:
                self.dom = self.reader.fromStream(input)
            if kw.get('keepdom', 0) == 0:
		self.dom.ZSI_reader = self.reader
        except Exception, e:
            # Is this in the header?  Your guess is as good as mine.
            raise ParseException("Can't parse document (" + \
                str(e.__class__) + "): " + str(e), 0)

        self.ns_cache = {
            id(self.dom): {
                'xml': XMLNS.XML,
                'xmlns': XMLNS.BASE,
                '': ''
            }
        }
        self.trailers, self.resolver, self.id_cache = \
            kw.get('trailers', 0), kw.get('resolver'), {}

        # Exactly one child element
        c = [ E for E in _children(self.dom)
                if E.nodeType == _Node.ELEMENT_NODE]
        if len(c) == 0:
            raise ParseException("Document has no Envelope", 0)
        if len(c) != 1:
            raise ParseException("Document has extra child elements", 0)

        # And that one child must be the Envelope
        elt = c[0]
        if elt.localName != "Envelope" \
        or elt.namespaceURI != SOAP.ENV:
            raise ParseException('Document has "' + elt.localName + \
                '" element, not Envelope', 0)
        self._check_for_legal_children("Envelope", elt)
        for a in _attrs(elt):
            name = a.nodeName
            if name.find(":") == -1 and name not in [ "xmlns", "id" ]:
                raise ParseException('Unqualified attribute "' + \
                        name + '" in Envelope', 0)
        self.envelope = elt
        if not _valid_encoding(self.envelope):
            raise ParseException("Envelope has invalid encoding", 0)

        # Get Envelope's child elements.
        c = [ E for E in _children(self.envelope)
                if E.nodeType == _Node.ELEMENT_NODE ]
        if len(c) == 0:
            raise ParseException("Envelope is empty (no Body)", 0)

        # Envelope's first child might be the header; if so, nip it off.
        elt = c[0]
        if elt.localName == "Header" \
        and elt.namespaceURI == SOAP.ENV:
            self._check_for_legal_children("Header", elt)
            self._check_for_pi_nodes(_children(elt), 1)
            self.header = c.pop(0)
            self.header_elements = _child_elements(self.header)
        else:
            self.header, self.header_elements = None, []

        # Now the first child must be the body
        if len(c) == 0:
            raise ParseException("Envelope has header but no Body", 0)
        elt = c.pop(0)
        if elt.localName != "Body" \
        or elt.namespaceURI != SOAP.ENV:
            if self.header:
                raise ParseException('Header followed by "' + \
                        elt.localName + \
                        '" element, not Body', 0, elt, self.dom)
            else:
                raise ParseException('Document has "' + \
                        elt.localName + \
                        '" element, not Body', 0, elt, self.dom)
        self._check_for_legal_children("Body", elt, 0)
        self._check_for_pi_nodes(_children(elt), 0)
        self.body = elt
        if not _valid_encoding(self.body):
            raise ParseException("Body has invalid encoding", 0)

        # Trailer elements.
        if not self.trailers:
            if len(c):
                raise ParseException("Element found after Body",
                        0, elt, self.dom)
            # Don't set self.trailer_elements = []; if user didn't ask
            # for trailers we *want* to throw an exception.
        else:
            self.trailer_elements = c
            for elt in self.trailer_elements:
                if not elt.namespaceURI:
                    raise ParseException('Unqualified trailer element',
                            0, elt, self.dom)

        # Find the serialization root.  Divide the Body children into
        # root (root=1), no (root=0), maybe (no root attribute).
        self.body_root, no, maybe = None, [], []
        for elt in _child_elements(self.body):
            root = _find_root(elt)
            if root == "1":
                if self.body_root:
                    raise ParseException("Multiple seralization roots found",
                            0, elt, self.dom)
                self.body_root = elt
            elif root == "0":
                no.append(elt)
            elif not root:
                maybe.append(elt)
            else:
                raise ParseException('Illegal value for root attribute',
                        0, elt, self.dom)

        # If we didn't find a root, get the first one that didn't
        # say "not me", unless they all said "not me."
        if self.body_root == None:
            if len(maybe):
                self.body_root = maybe[0]
            else:
                raise ParseException('No serialization root found',
                        0, self.body, self.dom)
        if not _valid_encoding(self.body_root):
            raise ParseException("Invalid encoding", 0,
                    elt, self.dom)

        # Now get all the non-roots (in order!).
        rootid = id(self.body_root)
        self.data_elements = [ E for E in _child_elements(self.body)
                                if id(E) != rootid ]
        self._check_for_pi_nodes(self.data_elements, 0)

    def __del__(self):
        try:
	    if hasattr(self.dom, 'ZSI_reader'):
		self.dom.ZSI_reader.releaseNode(self.dom)
		del self.dom.ZSI_reader
        except:
            pass

    def _check_for_legal_children(self, name, elt, mustqualify=1):
        '''Check if all children of this node are elements or whitespace-only
        text nodes.
        '''
        inheader = name == "Header"
        for n in _children(elt):
            t = n.nodeType
            if t == _Node.COMMENT_NODE: continue
            if t != _Node.ELEMENT_NODE:
                if t == _Node.TEXT_NODE and n.nodeValue.strip() == "":
                    continue
                raise ParseException("Non-element child in " + name, 
                        inheader, elt, self.dom)
            if mustqualify and not n.namespaceURI:
                raise ParseException('Unqualified element "' + \
                        n.nodeName + '" in ' + name, inheader, elt, self.dom)

    def _check_for_pi_nodes(self, list, inheader):
        '''Raise an exception if any of the list descendants are PI nodes.
        '''
        list = list[:]
        while list:
            elt = list.pop()
            t = elt.nodeType
            if t == _Node.PROCESSING_INSTRUCTION_NODE:
                raise ParseException('Found processing instruction "<?' + \
                        elt.nodeName + '...>"',
                        inheader, elt.parentNode, self.dom)
            elif t == _Node.DOCUMENT_TYPE_NODE:
                raise ParseException('Found DTD', inheader,
                        elt.parentNode, self.dom)
            list += _children(elt)

    def Backtrace(self, elt):
        '''Return a human-readable "backtrace" from the document root to
        the specified element.
        '''
        return _backtrace(elt, self.dom)

    def FindLocalHREF(self, href, elt, headers=1):
        '''Find a local HREF in the data elements.
        '''
        if href[0] != '#':
            raise EvaluateException(
                'Absolute HREF ("%s") not implemented' % href,
                self.Backtrace(elt))
        frag = href[1:]
        # Already found?
        e = self.id_cache.get(frag)
        if e: return e
        # Do a breadth-first search, in the data first.  Most likely
        # to find multi-ref targets shallow in the data area.
        list = self.data_elements[:] + [self.body_root]
        if headers: list.extend(self.header_elements)
        while list:
            e = list.pop()
            if e.nodeType == _Node.ELEMENT_NODE:
                nodeid = _find_id(e)
                if nodeid:
                    self.id_cache[nodeid] = e
                    if nodeid == frag: return e
            list += _children(e)
        raise EvaluateException('''Can't find node for HREF "%s"''' % href,
                self.Backtrace(elt))

    def ResolveHREF(self, uri, tc, **keywords):
        r = getattr(tc, 'resolver', self.resolver)
        if not r:
            raise EvaluateException('No resolver for "' + uri + '"')
        try:
            if type(uri) == types.UnicodeType: uri = str(uri)
            retval = r(uri, tc, self, **keywords)
        except Exception, e:
            raise EvaluateException('''Can't resolve "''' + uri + '" (' + \
                str(e.__class__) + "): " + str(e))
        return retval

    def GetMyHeaderElements(self, actorlist=None):
        '''Return a list of all elements intended for these actor(s).
        '''
        if actorlist == None:
            actorlist = [None, SOAP.ACTOR_NEXT]
        else:
            actorlist = list(actorlist) + [None, SOAP.ACTOR_NEXT]
        return [ E for E in self.header_elements
                if _find_actor(E) in actorlist ]

    def GetElementNSdict(self, elt):
        '''Get a dictionary of all the namespace attributes for the indicated
        element.  The dictionaries are cached, and we recurse up the tree
        as necessary.
        '''
        d = self.ns_cache.get(id(elt))
        if not d:
            if elt != self.dom: d = self.GetElementNSdict(elt.parentNode)
            for a in _attrs(elt):
                if a.namespaceURI == XMLNS.BASE:
                    if a.localName == "xmlns":
                        d[''] = a.nodeValue
                    else:
                        d[a.localName] = a.nodeValue
            self.ns_cache[id(elt)] = d
        return d.copy()

    def IsAFault(self):
        '''Is this a fault message?
        '''
        e = self.body_root
        if not e: return 0
        return e.namespaceURI == SOAP.ENV and e.localName == 'Fault'

    def Parse(self, how):
        '''Parse the message.
        '''
        if type(how) == types.ClassType: how = how.__dict__['typecode']
        return how.parse(self.body_root, self)

    def WhatMustIUnderstand(self):
        '''Return a list of (uri,localname) tuples for all elements in the
        header that have mustUnderstand set.
        '''
        return [ ( E.namespaceURI, E.localName )
                for E in self.header_elements if _find_mu(E) == "1" ]

    def WhatActorsArePresent(self):
        '''Return a list of URI's of all the actor attributes found in
        the header.  The special actor "next" is ignored.
        '''
        results = []
        for E in self.header_elements:
            a = _find_actor(E)
            if a not in [ None, SOAP.ACTOR_NEXT ]: results.append(a)
        return results

if __name__ == '__main__': print _copyright
