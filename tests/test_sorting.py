import os
from textwrap import dedent

from autosort.sorting import sort_imports


def test_regular():
    path = os.path.abspath('test.py')
    rv = sort_imports(dedent('''\
    from tokenize import COMMENT, INDENT, ENDMARKER
    from tokenize import (DEDENT,  # noqa
                          NEWLINE, STRING,
                          NAME)
    '''), path)

    assert rv == dedent('''\
    from tokenize import (COMMENT, DEDENT, ENDMARKER,     # noqa
                          INDENT, NAME, NEWLINE, STRING)  # noqa
    ''')


def test_name_order():
    path = os.path.abspath('test.py')
    rv = sort_imports(dedent('''\
    from a import CONST, CamelCase, snake_case, _priv, __dunder
    from ._priv import d
    from .sub import e
    from .. import f
    from . import g
    '''), path)

    assert rv == dedent('''\
    from a import CamelCase, snake_case, CONST, _priv, __dunder

    from .. import f
    from . import g
    from .sub import e
    from ._priv import d
    ''')


def test_sort_multiple_levels():
    path = os.path.abspath('test.py')
    rv = sort_imports(dedent('''\
    import a
    def f():
        import e
        if True:
            import c
            stmt = 4
            import d
        import b
    import f
    '''), path)

    assert rv == dedent('''\
    import a
    import f
    def f():
        import b
        import e
        if True:
            import c
            import d
            stmt = 4
    ''')


def test_skip_docstring():
    path = os.path.abspath('test.py')
    rv = sort_imports(dedent('''\
    """
        module docstring
    """
    import a
    def f():
        """Function docstring."""
        import e
        x = 2
        import b
    import f
    '''), path)

    assert rv == dedent('''\
    """
        module docstring
    """
    import a
    import f
    def f():
        """Function docstring."""
        import b
        import e
        x = 2
    ''')


def test_explicit_line_joinings():
    path = os.path.abspath('test.py')
    rv = sort_imports(dedent('''\
    from x import a as b, cc, \\
           d as e, e as f, g
    '''), path)

    assert rv == dedent('''\
    from x import a as b, cc, d as e, e as f, g
    ''')


def test_relative_import():
    path = os.path.abspath('test.py')
    rv = sort_imports(dedent('''\
    from . import x
    '''), path)

    assert rv == dedent('''\
    from . import x
    ''')


def test_source_with_header():
    path = os.path.abspath('test.py')
    rv = sort_imports(dedent('''\
    #!/usr/bin/env python
    # -*- coding: utf-8 -*-

    import x
    '''), path)

    assert rv == dedent('''\
    #!/usr/bin/env python
    # -*- coding: utf-8 -*-
    import x
    ''')
