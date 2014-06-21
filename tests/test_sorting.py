from autosort.sorting import sort_imports

from textwrap import dedent

import os


def test_regular():
    path = os.path.abspath('test.py')
    assert sort_imports(dedent('''
    from tokenize import COMMENT, DEDENT, ENDMARKER
    from tokenize import (INDENT,  # noqa
                          NEWLINE, STRING,
                          NAME)
    '''), path) == dedent('''\
    from tokenize import (COMMENT, DEDENT, ENDMARKER,     # noqa
                          INDENT, NAME, NEWLINE, STRING)  # noqa

    ''')
