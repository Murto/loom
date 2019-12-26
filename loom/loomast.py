#!/usr/bin/env python3

import abc
from collections import defaultdict
import enum

class AST(abc.ABC):
    
    @abc.abstractmethod
    def accept(self, visitor):
        pass

class Program(AST):
    
    def __init__(self, statements):
        self.statements = statements

    def __eq__(self, other):
        return self.statements == other.statements

    def accept(self, visitor):
        visitor.visit(self)

class LanguageDefinition(AST):

    def __init__(self, symbol, expression):
        self.symbol = symbol
        self.expression = expression

    def __eq__(self, other):
        return self.symbol == other.symbol \
            and self.expression == other.expression
    
    def accept(self, visitor):
        visitor.visit(self)

class StringDefinition(AST):
    
    def __init__(self, symbol, string_expression, set_expression):
        self.symbol = symbol
        self.string_expression = string_expression
        self.set_expression = set_expression

    def __eq__(self, other):
        return self.symbol == other.symbol  \
            and self.string_expression == other.string_expression \
            and self.set_expression == other.set_expression

    def accept(self, visitor):
        visitor.visit(self)

class UnionExpression(AST):
    
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __eq__(self, other):
        return self.left == other.left \
            and self.right == other.right

    def accept(self, visitor):
        visitor.visit(self)

class IntersectExpression(AST):
    
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __eq__(self, other):
        return self.left == other.left \
            and self.right == other.right;

    def accept(self, visitor):
        visitor.visit(self)

class ProductExpression(AST):
    
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __eq__(self, other):
        return self.left == other.left \
            and self.right == other.right;

    def accept(self, visitor):
        visitor.visit(self)

class DifferenceExpression(AST):
    
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __eq__(self, other):
        return self.left == other.left \
            and self.right == other.right;

    def accept(self, visitor):
        visitor.visit(self)

class ComplementExpression(AST):
    
    def __init__(self, expression):
        self.expression = expression

    def __eq__(self, other):
        return self.expression == other.expression

    def accept(self, visitor):
        visitor.visit(self)

class Set(AST):
    
    def __init__(self, expressions):
        self.expressions = expressions

    def __eq__(self, other):
        return self.expressions == other.expressions

    def accept(self, visitor):
        visitor.visit(self)

class Symbol(AST):

    def __init__(self, identifier):
        self.identifier = indentifier

    def __eq__(self, other):
        return self.identifier == other.identifier

    def accept(self, visitor):
        visitor.visit(self)

class ConcatenationExpression(AST):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __eq__(self, other):
        return self.left == other.left \
            and self.right == right

    def accept(self, visitor):
        visitor.visit(self)

class String(AST):

    def __init__(self, bits):
        self.bits = bits

    def __eq__(self, other):
        return self.bits == other.bits

    def accept(self, visitor):
        return visitor.visit(self)

class ASTStringifier:

    def visit(self, node):
        if type(node) == Program:
            return self.visit_program(node)
        elif type(node) == LanguageDefinition:
            return self.visit_language_definition(node)
        elif type(node) == StringDefinition:
            return self.visit_string_definition(node)
        elif type(node) == UnionExpression:
            return self.visit_union_expression(node)
        elif type(node) == IntersectExpression:
            return self.visit_intersect_expression(node)
        elif type(node) == ProductExpression:
            return self.visit_product_expression(node)
        elif type(node) == DifferenceExpression:
            return self.visit_difference_expression(node)
        elif type(node) == ComplementExpression:
            return self.visit_complement_expression(node)
        elif type(node) == ParenthesisExpression:
            return self.visit_parenthesis_expression(node)
        elif type(node) == Set:
            return self.visit_set(node)
        elif type(node) == Symbol:
            return self.visit_symbol(node)
        elif type(node) == ConcatenationExpression:
            return self.visit_concatenation_expression(node)
        elif type(node) == String:
            return self.visit_string(node)

    def visit_program(self, program):
        return f('<PROGRAM : '
                '{", ".join(s.accept(self) for s in program.statements)}>')

    def visit_language_definition(self, language_definition):
        return f('<LANGUAGE-DEFINITION : '
                '{language_definition.symbol.accept(self)}, '
                '{language_definition.expression.accept(self)}>')

    def visit_string_definition(self, string_definition):
        return f('<STRING-DEFINITION : '
                '{string_definition.symbol.accept(self)}, '
                '{string_definition.string_expression.accept(self)}, '
                '{string_definition.set_expression.accept(self)}>')
 
    def visit_union_expression(self, union_expression):
        return f('<UNION-EXPRESSION : '
                '{union_expression.left.accept(self)}, '
                '{union_expression.right.accept(self)}>')

    def visit_intersect_expression(self, intersect_expression):
        return f('<INTERSECT-EXPRESSION : '
                '{intersect_expression.left.accept(self)}, '
                '{intersect_expression.right.accept(self)}>')

    def visit_product_expression(self, product_expression):
        return f('<PRODUCT-EXPRESSION : '
                '{product_expression.left.accept(self)}, '
                '{product_expression.right.accept(self)}>')

    def visit_difference_expression(self, difference_expression):
        return f('<DIFFERENCE-EXPRESSION : '
                '{difference_expression.left.accept(self)}, '
                '{difference_expression.right.accept(self)}>')

    def visit_union_expression(self, complement_expression):
        return f('<COMPLEMENT-EXPRESSION : '
                '{complement_expression.expression.accept(self)}>')

    def visit_parenthesis_expression(self, parenthesis_expression):
        return f('<PARENTHESIS-EXPRESSION : '
                '{parenthesis_expression.expression.accept(self)}>')

    def visit_set(self, set):
        return f('<SET : '
                '{", ".join(e.accept(self) for e in set.expressions)}>')

    def visit_symbol(self, symbol):
        return f('<SYMBOL : '
                '{symbol.accept(this)}>')
    
    def visit_concatenation_expression(self, concatenation_expression):
        return f('<CONCATENATION-EXPRESSION : '
                '{concatenation_expression.left.accept(self), '
                '{concatenation_expression.right.accept(self)>')

    def visit_string(self, string):
        return f('<STRING : '
                '{"".join(str(bit) for bit in string.bits)}>')


class TypeChecker:

    class Type(enum.Enum):
        ALPHABET = enum.auto()
        LANGUAGE = enum.auto()
        STRING = enum.auto()
        TOKEN = enum.auto()
        
    def __init__(self):
        self.__symbols = set()
        self.__types = dict()
        self.__symbols.add('0')
        self.__symbols.add('1')
        self.types['0'] = TypeChecker.Type.TOKEN
        self.types['1'] = TypeChecker.Type.TOKEN

    def visit(self, node):
        if type(node) == Program:
            self.__visit_program(node)
        elif type(node) == AlphabetDefinition:
            self.__visit_alphabet_definition(node)
        elif type(node) == LanguageDefinition:
            self.__visit_language_definition(node)
        elif type(node) == StringDefinition:
            self.__visit_string_definition(node)
        elif type(node) == String:
            self.__visit_string(node)

    def __visit_program(self, program):
        for alphabet_definition in program.alphabet_definitions:
            alphabet_definition.accept(self)
        for language_definition in program.language_definitions:
            language_definition.accept(self)
        for string_definition in program.string_definitions:
            string_definition.accept(self)

    def __visit_alphabet_definition(self, alphabet_definition):
        for symbol in alphabet_definition.symbols:
            if symbol not in self.__symbols:
                raise RuntimeError('Token not declared')
            elif self.__types[symbol] != TypeChecker.Type.TOKEN:
                raise RuntimeError('Expected token')
        symbol = alphabet_definition.symbol
        if symbol in self.__symbols:
            raise RuntimeError('Symbol already declared')
        else:
            self.__symbols.add(symbol)
            self.__types[TypeChecker.Type.ALPHABET].add(symbol)
    
    def __visit_language_definition(self, language_definition):
        symbol = language_definition.symbol
        alphabet_symbol = language_definition.alphabet_symbol
        if symbol in self.__symbols:
            raise RuntimeError('Symbol already declared')
        elif alphabet_symbol not in self._alphabets:
            raise RuntimeError('Alphabet not declared')
        else:
            self.__symbols.add(symbol)
            self.languages.add(symbol)

    def __visit_string_definition(self, string_definition):
        symbol = string_definition.symbol
        language_symbol = string_definition.language_symbol
        if symbol in self.__symbols:
            raise RuntimeError('Symbol already declared')
        elif language_symbol not in self._languages:
            raise RuntimeError('Language not declared')
        else:
            self.__symbols.add(symbol)
            self._strings.add(symbol)

    def __visit_string(self, string):
        for symbol in string.symbols:
            if symbol not in self.__symbols:
                raise RuntimeError('Symbol not declared')
