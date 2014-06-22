import argparse
import sys

from .sorting import sort_imports


def create_parser():
    parser = argparse.ArgumentParser(prog='autosort')
    parser.add_argument('files', nargs='+')
    return parser


def parse_args(args):
    parser = create_parser()
    args = parser.parse_args(args)
    return args


def main():
    args = parse_args(sys.argv[1:])
    for file in args.files:
        with open(file) as f:
            output = sort_imports(f.read(), file)
        with open(file, 'w') as f:
            f.write(output)
