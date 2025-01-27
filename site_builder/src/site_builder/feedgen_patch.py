from feedgen.util import xml_elem
from feedgen.entry import _add_text_elm

def atom_entry_patched(self, extensions=True):
    '''Create an ATOM entry and return it.'''
    entry = xml_elem('entry')
    if not (self._FeedEntry__atom_id and self._FeedEntry__atom_title and self._FeedEntry__atom_updated):
        raise ValueError('Required fields not set')
    id = xml_elem('id', entry)
    id.text = self._FeedEntry__atom_id
    title = xml_elem('title', entry)
    title.text = self._FeedEntry__atom_title
    updated = xml_elem('updated', entry)
    updated.text = self._FeedEntry__atom_updated.isoformat()

    # An entry must contain an alternate link if there is no content
    # element.
    if not self._FeedEntry__atom_content:
        links = self._FeedEntry__atom_link or []
        if not [link for link in links if link.get('rel') == 'alternate']:
            raise ValueError('Entry must contain an alternate link or '
                                'a content element.')

    # Add author elements
    for a in self._FeedEntry__atom_author or []:
        # Atom requires a name. Skip elements without.
        if not a.get('name'):
            continue
        author = xml_elem('author', entry)
        name = xml_elem('name', author)
        name.text = a.get('name')
        if a.get('email'):
            email = xml_elem('email', author)
            email.text = a.get('email')
        if a.get('uri'):
            uri = xml_elem('uri', author)
            uri.text = a.get('uri')

    _add_text_elm(entry, self._FeedEntry__atom_content, 'content')

    for link in self._FeedEntry__atom_link or []:
        _link = xml_elem('link', entry, href=link['href'])
        if link.get('rel'):
            _link.attrib['rel'] = link['rel']
        if link.get('type'):
            _link.attrib['type'] = link['type']
        if link.get('hreflang'):
            _link.attrib['hreflang'] = link['hreflang']
        if link.get('title'):
            _link.attrib['title'] = link['title']
        if link.get('length'):
            _link.attrib['length'] = link['length']

    _add_text_elm(entry, self._FeedEntry__atom_summary, 'summary')

    for c in self._FeedEntry__atom_category or []:
        cat = xml_elem('category', entry, term=c['term'])
        if c.get('scheme'):
            cat.attrib['scheme'] = c['scheme']
        if c.get('label'):
            cat.attrib['label'] = c['label']

    # Add author elements
    for c in self._FeedEntry__atom_contributor or []:
        # Atom requires a name. Skip elements without.
        if not c.get('name'):
            continue
        contrib = xml_elem('contributor', entry)
        name = xml_elem('name', contrib)
        name.text = c.get('name')
        if c.get('email'):
            email = xml_elem('email', contrib)
            email.text = c.get('email')
        if c.get('uri'):
            uri = xml_elem('uri', contrib)
            uri.text = c.get('uri')

    if self._FeedEntry__atom_published:
        published = xml_elem('published', entry)
        published.text = self._FeedEntry__atom_published.isoformat()

    if self._FeedEntry__atom_rights:
        rights = xml_elem('rights', entry)
        rights.text = self._FeedEntry__atom_rights

    if self._FeedEntry__atom_source:
        source = xml_elem('source', entry)
        if self._FeedEntry__atom_source.get('title'):
            source_title = xml_elem('title', source)
            source_title.text = self._FeedEntry__atom_source['title']
        if self._FeedEntry__atom_source.get('link'):
            xml_elem('link', source, href=self._FeedEntry__atom_source['link'])

    if extensions:
        for ext in self._FeedEntry__extensions.values() or []:
            if ext.get('atom'):
                ext['inst'].extend_atom(entry)

    return entry

    '''Create an ATOM entry and return it.'''
    entry = xml_elem('entry')
    if not (self._FeedEntry__atom_id and self._FeedEntry__atom_title and self._FeedEntry__atom_updated):
        raise ValueError('Required fields not set')
    id = xml_elem('id', entry)
    id.text = self._FeedEntry__atom_id
    title = xml_elem('title', entry)
    title.text = self._FeedEntry__atom_title
    updated = xml_elem('updated', entry)
    updated.text = self._FeedEntry__atom_updated.isoformat()

    # An entry must contain an alternate link if there is no content
    # element.
    if not self._FeedEntry__atom_content:
        links = self._FeedEntry__atom_link or []
        if not [link for link in links if link.get('rel') == 'alternate']:
            raise ValueError('Entry must contain an alternate link or '
                                'a content element.')

    # Add author elements
    for a in self._FeedEntry__atom_author or []:
        # Atom requires a name. Skip elements without.
        if not a.get('name'):
            continue
        author = xml_elem('author', entry)
        name = xml_elem('name', author)
        name.text = a.get('name')
        if a.get('email'):
            email = xml_elem('email', author)
            email.text = a.get('email')
        if a.get('uri'):
            uri = xml_elem('uri', author)
            uri.text = a.get('uri')

    _add_text_elm(entry, self._FeedEntry__atom_content, 'content')

    for link in self._FeedEntry__atom_link or []:
        _link = xml_elem('link', entry, href=link['href'])
        if link.get('rel'):
            _link.attrib['rel'] = link['rel']
        if link.get('type'):
            _link.attrib['type'] = link['type']
        if link.get('hreflang'):
            _link.attrib['hreflang'] = link['hreflang']
        if link.get('title'):
            _link.attrib['title'] = link['title']
        if link.get('length'):
            _link.attrib['length'] = link['length']

    _add_text_elm(entry, self._FeedEntry__atom_summary, 'summary')

    for c in self._FeedEntry__atom_category or []:
        cat = xml_elem('category', entry, term=c['term'])
        if c.get('scheme'):
            cat.attrib['scheme'] = c['scheme']
        if c.get('label'):
            cat.attrib['label'] = c['label']

    # Add author elements
    for c in self._FeedEntry__atom_contributor or []:
        # Atom requires a name. Skip elements without.
        if not c.get('name'):
            continue
        contrib = xml_elem('contributor', entry)
        name = xml_elem('name', contrib)
        name.text = c.get('name')
        if c.get('email'):
            email = xml_elem('email', contrib)
            email.text = c.get('email')
        if c.get('uri'):
            uri = xml_elem('uri', contrib)
            uri.text = c.get('uri')

    if self._FeedEntry__atom_published:
        published = xml_elem('published', entry)
        published.text = self._FeedEntry__atom_published.isoformat()

    if self._FeedEntry__atom_rights:
        rights = xml_elem('rights', entry)
        rights.text = self._FeedEntry__atom_rights

    if self._FeedEntry__atom_source:
        source = xml_elem('source', entry)
        if self._FeedEntry__atom_source.get('title'):
            source_title = xml_elem('title', source)
            source_title.text = self._FeedEntry__atom_source['title']
        if self._FeedEntry__atom_source.get('link'):
            xml_elem('link', source, href=self._FeedEntry__atom_source['link'])

    if extensions:
        for ext in self._FeedEntry__extensions.values() or []:
            if ext.get('atom'):
                ext['inst'].extend_atom(entry)

    return entry