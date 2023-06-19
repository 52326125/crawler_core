from enum import Enum


class HTMLParser(str, Enum):
    DEFAULT = "html.parser"
    LXML = "lxml"
    HTML5LIB = "html5lib"
