#!/usr/bin/env python3

import argparse
import enum
import re
import sys


class TokenType(enum.Enum):
    LET = 0
    ASSIGN = 1
    NEWLINE = 2
    LEFT_BRACE = 3
    RIGHT_BRACE = 4
    ASTERISK = 5
    IN = 6
    COMMA = 7
    SYMBOL = 8
    CHARACTER = 9
    STRING = 10

class Token:

    def __init__(self, type, value):
        self.type = type
        self.value = value


def tokenize(source):
    token_map = {
        re.compile('let') : TokenType.LET,
        re.compile('=') : TokenType.ASSIGN,
        re.compile('\n') : TokenType.NEWLINE,
        re.compile('{') : TokenType.LEFT_BRACE,
        re.compile('}') : TokenType.RIGHT_BRACE,
        re.compile('\\*') : TokenType.ASTERISK,
        re.compile('in') : TokenType.IN,
        re.compile(',') : TokenType.COMMA,
        re.compile('\\w+') : TokenType.SYMBOL,
        re.compile('\'\\S\'') : TokenType.CHARACTER,
        re.compile('"\\S*"') : TokenType.STRING
    }
    while len(source) > 0:
        for pattern, type in token_map.items():
            result = pattern.match(source)
            if result:
                value = result.group()
                source = source[result.end:]
                yield Token(type, value)

def parse_arguments():
    description = 'Loom is a toy programming language by Murray Steele'
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
        for line in source:
            print(line.strip())

if __name__ == '__main__':
    main()
