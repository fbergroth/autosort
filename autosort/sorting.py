import re

from .config import get_config
from .formatting import format_group
from .parsing import parse_imports
from .utils import interpose, ordered_subgroups

_is_encoding_decl = re.compile(r'coding[=:]\s*([-\w.]+)').search


def sort_imports(source, path):
    config = get_config(path)
    lines = source.splitlines(True)
    header = extract_header(lines)
    diff = []
    ADD, REMOVE = range(2)
    for block in parse_imports(lines):
        diff += [(start, REMOVE, end, [])
                 for start, end in removals(block.imports, lines)]
        diff += [(line, ADD, line, rows)
                 for line, rows in organize_block(block, lines, config)]

    for start, kind, end, change in sorted(diff, reverse=True):
        lines[start:end] = change

    return ''.join(header + lines)


def extract_header(lines):
    header = []
    if lines and lines[0].startswith('#!'):
        header.append(lines.pop(0))

    if lines and _is_encoding_decl(lines[0]):
        header.append(lines.pop(0))

    while lines and lines[0] == '\n':
        lines.pop(0)

    return header


def removals(imports, lines):
    for im in imports:
        yield im.start, im.end

    for im1, im2 in zip(imports, imports[1:]):
        start, end = im1.end, im2.start
        if all(line == '\n' for line in lines[start:end]):
            yield start, end


def organize_block(block, lines, config):
    def sort(group):
        return sort_group(group, block.indent, config)

    regular, groups = extract_groups(block, lines)
    regulars = ordered_subgroups(regular, lambda im: im.module.kind(config))

    return ([(g[0].start, sort(g)) for g in groups] +
            [(block.start, interpose([sort(g) for g in regulars], ['\n']))])


def flatten(imports):
    result = {}
    for im in imports:
        result[im.module] = result.get(im.module, im).merge(im)
    return sorted(result.values())


def sort_group(group, indent, config):
    imports = flatten([im for im in group if im.kind == 'import'])
    froms = flatten([im for im in group if im.kind == 'from'])

    return (format_group('import', imports, indent, config) +
            format_group('from', froms, indent, config))


def cut_group(imports, index):
    j = index + 1
    while j < len(imports) and imports[j].start == imports[j-1].end:
        j += 1
    res, imports[index:j] = imports[index:j], []
    return res


def extract_groups(block, lines):
    index = 0
    groups = []
    imports = block.imports
    while index < len(imports):
        start = imports[index].start
        if start > 0 and lines[start - 1].startswith(block.indent + '#'):
            groups.append(cut_group(imports, index))
        else:
            index += 1

    return imports, groups
