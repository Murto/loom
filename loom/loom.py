#!/usr/bin/env python3

import argparse
import sys

from loomtoken import tokenize
from loomparse import parse
from loomast import print_ast, typecheck_ast
from loomgen import generate_program

def parse_arguments():
    description = 'Loom is a programming language by Murray Steele'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('source_file',
                        metavar='source_file',
                        type=str,
                        help='Loom source file')
    parser.add_argument('--ast',
                        action='store_true',
                        default=False,
                        help='Print string representation of abstract syntax tree')
    parser.add_argument('-o',
                        metavar='output',
                        type=str,
                        dest='output',
                        help='Output python file')
    args = parser.parse_args()
    return vars(args)

def main():
    arguments = parse_arguments()
    with open(arguments['source_file']) as source:
        tokens = list(tokenize(source.read()))
        tree = parse(tokens)
        if arguments['ast']:
            print_ast(tree)
        else:
            typecheck_ast(tree)
            program = generate_program(tree)
            if arguments['output']:
                with open(arguments['output'], 'w') as output:
                    output.write(program)
            else:
                print(program)



if __name__ == '__main__':
    main()
