# pylint: disable=too-few-public-methods
"""
Operation classes must be defined in this module.

In a future version we might consider adding support for fully qualified paths
when creating a Pipeline, e.g.:
Pipeline['CleanText', 'my.org.package.OperationClass'])

so that users do not have to put their Operation classes inside of this module.
"""


class Operation:
    """
    Base class for pipeline operations.
    """

    def __call__(self, doc):
        raise NotImplementedError()


class Language(Operation):
    """
    Extract the language from a text

    >>> from textpipe.doc import Doc
    >>> doc = Doc('Test sentence for testing text')
    >>> Language()(doc)
    'en'
    """

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __call__(self, doc):
        return doc.language


class CleanText(Operation):
    """
    Clean HTML and normalise punctuation.

    >>> from textpipe.doc import Doc
    >>> doc = Doc('“Please clean this piece… of text</b>„')
    >>> CleanText()(doc)
    '"Please clean this piece... of text"'
    """

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __call__(self, doc):
        return doc.clean


class Raw(Operation):
    """
    Extract the number of words from text

    >>> from textpipe.doc import Doc
    >>> doc = Doc('Test sentence for testing text')
    >>> Raw()(doc)
    'Test sentence for testing text'
    """

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __call__(self, doc):
        return doc.raw


class NWords(Operation):
    """
    Extract the number of words from text

    >>> from textpipe.doc import Doc
    >>> doc = Doc('Test sentence for testing text')
    >>> NWords()(doc)
    5
    """

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __call__(self, doc):
        return doc.nwords


class Words(Operation):
    """
    Extract words from text

    >>> from textpipe.doc import Doc
    >>> doc = Doc('Test sentence for testing text')
    >>> Words()(doc)
    [('Test', 0), ('sentence', 5), ('for', 14), ('testing', 18), ('text', 26)]
    """

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __call__(self, doc):
        return doc.words


class WordCounts(Operation):
    """
    Extract words with their counts

    >>> from textpipe.doc import Doc
    >>> doc = Doc('Test sentence for testing vectorisation of a sentence.')
    >>> WordCounts()(doc)
    {'Test': 1, 'sentence': 2, 'for': 1, 'testing': 1, 'vectorisation': 1, 'of': 1, 'a': 1, '.': 1}
    """

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __call__(self, doc):
        return doc.word_counts


class Complexity(Operation):
    """
    Determine the complexity of text using the Flesch
    reading ease test ranging from 0.0 - 100.0 with 0.0
    being the most difficult to read.

    >>> from textpipe.doc import Doc
    >>> doc = Doc('Test sentence for testing text')
    >>> Complexity()(doc)
    83.32000000000004
    """

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __call__(self, doc):
        return doc.complexity


class Sentences(Operation):
    """
    Extract sentences from text

    >>> from textpipe.doc import Doc
    >>> doc = Doc('Test sentence for testing text. And another one with, some, punctuation! And stuff.')
    >>> Sentences()(doc)
    [('Test sentence for testing text.', 0), ('And another one with, some, punctuation!', 32), ('And stuff.', 73)]
    """

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __call__(self, doc):
        return doc.sents


class NSentences(Operation):
    """
    Extract the number of sentences from text

    >>> from textpipe.doc import Doc
    >>> doc = Doc('Test sentence for testing text')
    >>> NSentences()(doc)
    1
    """

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __call__(self, doc):
        return doc.nsents


class Entities(Operation):
    """
    Extract a list of the named entities in text

    >>> from textpipe.doc import Doc
    >>> doc = Doc('Sentence for testing Google text')
    >>> Entities()(doc)
    [('Google', 'ORG')]
    """

    def __init__(self, model_mapping=None, **kwargs):
        self.kwargs = kwargs
        self.model_mapping = model_mapping

    def __call__(self, doc):
        lang = doc.language if doc.is_reliable_language else doc.hint_language
        return doc.find_ents(self.model_mapping[lang]) if self.model_mapping else doc.ents


class Sentiment(Operation):
    """
    Returns polarity score (-1 to 1) and a subjectivity score (0 to 1)

    Currently only English, Dutch, French and Italian supported

    >>> from textpipe.doc import Doc
    >>> doc = Doc('Een hele leuke test zin.')
    >>> Sentiment()(doc)
    (0.9599999999999999, 1.0)
    """

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __call__(self, doc):
        return doc.sentiment


class Keyterms(Operation):
    """
    Returns a list of up to 10 key terms extracted from the document. This
    works on any language the Doc can tokenize.

    >>> from textpipe.doc import Doc
    >>> doc = Doc('Amsterdam is the awesome capital of the Netherlands.')
    >>> Keyterms()(doc)
    [('awesome', 0.32456160227748454), ('capital', 0.32456160227748454), ('amsterdam', 0.17543839772251532), ('netherlands', 0.17543839772251532)]
    >>> Keyterms(n_terms=2)(doc)
    [('awesome', 0.32456160227748454), ('capital', 0.32456160227748454)]
    >>> Keyterms(ranker='sgrank')(doc)
    [('awesome capital', 0.5638711013322963), ('netherlands', 0.22636566128805719), ('amsterdam', 0.20976323737964653)]
    """

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __call__(self, doc):
        return doc.extract_keyterms(**self.kwargs)
