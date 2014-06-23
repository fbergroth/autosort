import argparse
import sys

from .sorting import sort_imports


def create_parser():
    parser = argparse.ArgumentParser(prog='autosort')
    parser.add_argument('files', nargs='+')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='show verbose output')
    return parser


def parse_args(args):
    parser = create_parser()
    args = parser.parse_args(args)
    return args


def main():
    args = parse_args(sys.argv[1:])
    for file in args.files:
        with open(file) as f:
            input = f.read()

        output = sort_imports(input, file)
        changed = input != output

        if changed:
            with open(file, 'w') as f:
                f.write(output)

        if args.verbose:
            print('{0} {1}'.format('>>>' if changed else '...', file))
