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
    line = 1;
    column = 1;
    while len(source) > 0:
        token = None
        for pattern, type in token_map.items():
            result = pattern.match(source)
            if result:
                value = result.group()
                column += len(value)
                source = source[len(value):]
                token = Token(type, value)
                break
        if token is not None:
            if token.type == TokenType.NEWLINE:
                line += 1
                column = 1;
            yield Token(type, value)
        else:
            raise RuntimeError(f'Unknown token at line {line} column {column}')


