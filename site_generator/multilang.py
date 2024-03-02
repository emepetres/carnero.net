from feedgen.ext.base import BaseEntryExtension, BaseExtension


class MultilangExtension(BaseExtension):
    '''FeedGenerator extension for multi language feeds.'''
    pass


class MultilangEntryExtension(BaseEntryExtension):
    '''FeedEntry extension for lang tag.
    '''

    def __init__(self):
        self.__lang = None

    def extend_atom(self, entry):
        '''Add additional lang tag to an RSS item.

        :param feed: The RSS item XML element to use.
        '''

        if self.__lang:
            entry.attrib['{http://www.w3.org/XML/1998/namespace}lang'] = self.__lang

        return entry

    def extend_rss(self, item):
        return self.extend_atom(item)

    def language(self, language:str=None):
        '''Get or set the language of the entry. It indicates the language the
        post is written in. This allows aggregators to group all Spanish
        language entries, for example, on a single page. This value will also be used to set the xml:lang
        property of the ATOM or RSS entry node.
        The value should be an IETF language tag.

        :param language: Language of the entry.
        :returns: Language of the entry.
        '''
        if language is None:
            return self.__lang
        self.__lang = language