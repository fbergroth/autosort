import os
from textwrap import dedent

from autosort.sorting import sort_imports


def test_regular():
    path = os.path.abspath('test.py')
    rv = sort_imports(dedent('''
    from tokenize import COMMENT, INDENT, ENDMARKER
    from tokenize import (DEDENT,  # noqa
                          NEWLINE, STRING,
                          NAME)
    '''), path)

    assert rv == dedent('''\
    from tokenize import (COMMENT, DEDENT, ENDMARKER,     # noqa
                          INDENT, NAME, NEWLINE, STRING)  # noqa

    ''')
