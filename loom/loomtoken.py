#!/usr/bin/env python3

import abc
import enum
import re

class TokenType(enum.Enum):
    NEWLINE           = enum.auto() 
    SYMBOL            = enum.auto() 
    DEFINE            = enum.auto()
    IN                = enum.auto() 
    UNION             = enum.auto()
    INTERSECT         = enum.auto()
    PRODUCT           = enum.auto()
    DIFFERENCE        = enum.auto()
    COMPLEMENT        = enum.auto()
    LEFT_PARENTHESIS  = enum.auto() 
    RIGHT_PARENTHESIS = enum.auto() 
    LEFT_BRACE        = enum.auto() 
    RIGHT_BRACE       = enum.auto() 
    EMPTY_SET         = enum.auto() 
    EMPTY_STRING      = enum.auto() 
    COMMA             = enum.auto() 
    STRING            = enum.auto() 


class Token(abc.ABC):
    pass

class Newline(Token):
    
    def __repr__(self):
        return '<Newline>'

class Symbol(Token):

    def __init__(self, symbol):
        self.symbol = symbol

    def __repr__(self):
        return f'<Symbol : {self.symbol}>'

class Define(Token):

    def __repr__(self):
        return '<Define>'

class In(Token):
    
    def __repr__(self):
        return '<In>'

class Union(Token):

    def __repr__(self):
        return '<Union>'

class Intersect(Token):
    
    def __repr__(self):
        return '<Intersect>'

class Product(Token):

    def __repr__(self):
        return '<Product>'

class Difference(Token):
    
    def __repr__(self):
        return '<Difference>'

class Complement(Token):
    
    def __repr__(self):
        return '<Complement>'

class LeftParenthesis(Token):

    def __repr__(self):
        return '<Left Parenthesis>'

class RightParenthesis(Token):
    
    def __repr__(self):
        return '<Right Parenthesis>'

class LeftBrace(Token):
    
    def __repr__(self):
        return '<Left Brace>'


class RightBrace(Token):

    def __repr__(self):
        return '<Right Brace>'

class EmptySet(Token):

    def __repr__(self):
        return '<Empty Set>'

class Comma(Token):
    
    def __repr__(self):
        return '<Comma>'

class String(Token):

    def __init__(self, data):
        self.value = list()
        for c in data:
            self.value.append(int(c))
    
    def __repr__(self):
        if self.value:
            return f'<String : {"".join(str(x) for x in self.value)}>'
        else:
            return '<String : ε>'

def make_token(type, value):
    if type == TokenType.NEWLINE:
        return Newline()
    elif type == TokenType.SYMBOL:
        return Symbol(value)
    elif type == TokenType.DEFINE:
        return Define()
    elif type == TokenType.IN:
        return In()
    elif type == TokenType.UNION:
        return Union()
    elif type == TokenType.INTERSECT:
        return Intersect()
    elif type == TokenType.PRODUCT:
        return Product()
    elif type == TokenType.DIFFERENCE:
        return Difference()
    elif type == TokenType.COMPLEMENT:
        return Complement()
    elif type == TokenType.LEFT_PARENTHESIS:
        return LeftParenthesis()
    elif type == TokenType.RIGHT_PARENTHESIS:
        return RightParenthesis()
    elif type == TokenType.LEFT_BRACE:
        return LeftBrace()
    elif type == TokenType.RIGHT_BRACE:
        return RightBrace()
    elif type == TokenType.EMPTY_SET:
        return EmptySet()
    elif type == TokenType.EMPTY_STRING:
        return String('')
    elif type == TokenType.COMMA:
        return Comma()
    elif type == TokenType.STRING:
        return String(value)
    else:
        raise RuntimeError(f'Invalid token type {type}')


def tokenize(source):
    type_map = {
        re.compile('\n') : TokenType.NEWLINE,
        re.compile(':=') : TokenType.DEFINE,
        re.compile('∈') : TokenType.IN,
        re.compile('∪') : TokenType.UNION,
        re.compile('∩') : TokenType.INTERSECT,
        re.compile('-') : TokenType.DIFFERENCE,
        re.compile('¬') : TokenType.COMPLEMENT,
        re.compile('\\(') : TokenType.LEFT_PARENTHESIS,
        re.compile('\\)') : TokenType.RIGHT_PARENTHESIS,
        re.compile('{') : TokenType.LEFT_BRACE,
        re.compile('}') : TokenType.RIGHT_BRACE,
        re.compile('∅') : TokenType.EMPTY_SET,
        re.compile('ε') : TokenType.EMPTY_STRING,
        re.compile(',') : TokenType.COMMA,
        re.compile('(1|0)+') : TokenType.STRING,
        re.compile('[a-zA-Z_]+') : TokenType.SYMBOL,
    }
    line = 1
    column = 1
    while len(source) > 0:
        if source[0] in ' \t':
            source = source[1:]
        else:
            found = False
            for pattern, type in type_map.items():
                result = pattern.match(source)
                if result:
                    if type == TokenType.NEWLINE:
                        line += 1
                        column = 1;
                    value = result.group()
                    column += len(value)
                    source = source[len(value):]
                    yield make_token(type, value)
                    found = True
                    break
            if not found:
                raise RuntimeError(f'Unknown token at line {line} column {column}')
