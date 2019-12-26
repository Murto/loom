#!/usr/bin/env python3

import argparse
import sys

from loomtoken import tokenize
from loomparse import parse
from loomast import ASTStringifier, TypeChecker

def parse_arguments():
    description = 'Loom is a programming language by Murray Steele'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('source_file',
                        metavar='source_file',
                        type=str,
                        help='Loom source file')
    args = parser.parse_args()
    return vars(args)

def main():
    arguments = parse_arguments()
    with open(arguments['source_file']) as source:
        tokens = list(tokenize(source.read()))
        print(tokens)

if __name__ == '__main__':
    main()
