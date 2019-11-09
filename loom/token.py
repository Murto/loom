#!/usr/bin/env python3

import enum
import re

class TokenType(enum.Enum):
    LET         = enum.auto()
    ASSIGN      = enum.auto()
    NEWLINE     = enum.auto() 
    LEFT_BRACE  = enum.auto() 
    RIGHT_BRACE = enum.auto() 
    ASTERISK    = enum.auto() 
    IN          = enum.auto() 
    COMMA       = enum.auto() 
    SYMBOL      = enum.auto() 
    CHARACTER   = enum.auto() 
    STRING      = enum.auto() 

class Token:

    def __init__(self, type, value):
        self.type = type
        self.value = value


def tokenize(source):
    type_map = {
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
    line = 1;
    column = 1;
    tokens = list()
    while len(source) > 0:
        if source[0] in " \t":
            source = source[1:]
        else:
            found = False
            for pattern, type in type_map.items():
                result = pattern.match(source)
                if result:
                    value = result.group()
                    column += len(value)
                    source = source[len(value):]
                    tokens.append(Token(type, value))
                    if type == TokenType.NEWLINE:
                        line += 1
                        column = 1;
                    found = True
                    break
            if not found:
                raise RuntimeError(f'Unknown token at line {line} column {column}')
    return tokens
