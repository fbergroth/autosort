import ast
import textwrap
import tokenize
from collections import namedtuple
from tokenize import COMMENT, DEDENT, ENDMARKER, INDENT, NAME, NEWLINE, STRING

from .data import Block, Import, Module, Name


def parse_imports(lines):
    it = iter(lines)
    tokens = (_TokenInfo(*token) for token in
              tokenize.generate_tokens(lambda: next(it)))

    result = []
    _ImportParser(tokens, lines).parse_block('', 0, result)
    return result


class _TokenInfo(namedtuple('TokenInfo', 'type string start end line')):
    @property
    def name(self):
        return self.type == NAME and self.string

    @property
    def starts_block(self):
        return self.type == INDENT

    @property
    def ends_block(self):
        return self.type in (DEDENT, ENDMARKER)


class _ImportParser(namedtuple('_ImportParser', 'tokens lines')):
    def parse_block(self, indent, start, result):
        imports = []
        token = next(self.tokens)

        # Push imports beneath docstring
        if token.type == STRING:
            start = token.end[0]
            token = next(self.tokens)

        while not token.ends_block:
            if token.starts_block:
                self.parse_block(token.string, token.start[0] - 1, result)
            elif token.name in ('from', 'import'):
                imports += self.parse_imports(token)
            token = next(self.tokens)

        if imports:
            result.append(Block(imports, indent, start))

    def parse_imports(self, token):
        first = token
        comments = []
        while token.type != NEWLINE:
            if token.type == COMMENT:
                comments.append(token.string)
            token = next(self.tokens)

        start, end = first.start[0] - 1, token.end[0]
        source = ''.join(self.lines[start:end])
        nodes = ast.parse(textwrap.dedent(source)).body
        # TODO: error on multiple nodes
        return self._make_imports(first.name, nodes[0], comments, start, end)

    @staticmethod
    def _make_imports(kind, node, comments, start, end):
        noqa = any(c.startswith('# noqa') for c in comments)
        names = sorted([Name(n.name, n.asname)
                        for n in node.names], key=Name.key)
        if kind == 'from':
            modules = [Module(Name(node.module or '', None), node.level)]
        else:
            modules, names = [Module(name, 0) for name in names], []

        return [Import(kind, m, names, noqa, start, end) for m in modules]
