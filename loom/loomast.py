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
        return visitor.visit(self)

class LanguageDefinition(AST):

    def __init__(self, symbol, expression):
        self.symbol = symbol
        self.expression = expression

    def __eq__(self, other):
        return self.symbol == other.symbol \
            and self.expression == other.expression
    
    def accept(self, visitor):
        return visitor.visit(self)

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
        return visitor.visit(self)

class ExclaimStatement(AST):

    def __init__(self, expression):
        self.expression = expression

    def __eq__(self, other):
        return self.expression == other.expression

    def accept(self, visitor):
        return visitor.visit(self)

class InquireStatement(AST):

    def __init__(self, symbol, expression):
        self.symbol = symbol
        self.expression = expression

    def __eq__(self, other):
        return self.symbol == other.symbol \
            and self.expression == other.expression

    def accept(self, visitor):
        return visitor.visit(self)

class UnionExpression(AST):
    
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __eq__(self, other):
        return self.left == other.left \
            and self.right == other.right

    def accept(self, visitor):
        return visitor.visit(self)

class IntersectExpression(AST):
    
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __eq__(self, other):
        return self.left == other.left \
            and self.right == other.right;

    def accept(self, visitor):
        return visitor.visit(self)

class ProductExpression(AST):
    
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __eq__(self, other):
        return self.left == other.left \
            and self.right == other.right;

    def accept(self, visitor):
        return visitor.visit(self)

class DifferenceExpression(AST):
    
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __eq__(self, other):
        return self.left == other.left \
            and self.right == other.right;

    def accept(self, visitor):
        return visitor.visit(self)

class ComplementExpression(AST):
    
    def __init__(self, expression):
        self.expression = expression

    def __eq__(self, other):
        return self.expression == other.expression

    def accept(self, visitor):
        return visitor.visit(self)

class KleeneExpression(AST):

    def __init__(self, expression):
        self.expression = expression

    def __eq__(self, other):
        return self.expression == other.expression

    def accept(self, visitor):
        return visitor.visit(self)

class Set(AST):
    
    def __init__(self, expressions):
        self.expressions = expressions

    def __eq__(self, other):
        return self.expressions == other.expressions

    def accept(self, visitor):
        return visitor.visit(self)

class Symbol(AST):

    def __init__(self, identifier):
        self.identifier = identifier

    def __eq__(self, other):
        return self.identifier == other.identifier

    def __hash__(self):
        return hash(self.identifier)

    def accept(self, visitor):
        return visitor.visit(self)

class ConcatenateExpression(AST):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __eq__(self, other):
        return self.left == other.left \
            and self.right == other.right

    def accept(self, visitor):
        return visitor.visit(self)

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
        elif type(node) == ExclaimStatement:
            return self.visit_exclaim_statement(node)
        elif type(node) == InquireStatement:
            return self.visit_inquire_statement(node)
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
        elif type(node) == KleeneExpression:
            return self.visit_kleene_expression(node)
        elif type(node) == Set:
            return self.visit_set(node)
        elif type(node) == Symbol:
            return self.visit_symbol(node)
        elif type(node) == ConcatenateExpression:
            return self.visit_concatenate_expression(node)
        elif type(node) == String:
            return self.visit_string(node)
        raise RuntimeError('Unknown node type')

    def visit_program(self, program):
        return f'(PROGRAM : {", ".join([ s.accept(self) for s in program.statements ])})'

    def visit_language_definition(self, language_definition):
        return '(LANGUAGE-DEFINITION : ' \
                f'{language_definition.symbol.accept(self)}, ' \
                f'{language_definition.expression.accept(self)})'

    def visit_string_definition(self, string_definition):
        return '(STRING-DEFINITION : ' \
                f'{string_definition.symbol.accept(self)}, ' \
                f'{string_definition.string_expression.accept(self)}, ' \
                f'{string_definition.set_expression.accept(self)})'
 
    def visit_exclaim_statement(self, exclaim_statement):
        return '(EXCLAIM-STATEMENT : ' \
                f'{exclaim_statement.expression.accept(self)})'

    def visit_inquire_statement(self, inquire_statement):
        return '(INQUIRE-STATEMENT : ' \
                f'{inquire_statement.symbol.accept(self)}, ' \
                f'{inquire_statement.expression.accept(self)})'

    def visit_union_expression(self, union_expression):
        return '(UNION-EXPRESSION : ' \
                f'{union_expression.left.accept(self)}, ' \
                f'{union_expression.right.accept(self)})'

    def visit_intersect_expression(self, intersect_expression):
        return '(INTERSECT-EXPRESSION : ' \
                f'{intersect_expression.left.accept(self)}, ' \
                f'{intersect_expression.right.accept(self)})'

    def visit_product_expression(self, product_expression):
        return '(PRODUCT-EXPRESSION : ' \
                f'{product_expression.left.accept(self)}, ' \
                f'{product_expression.right.accept(self)})'

    def visit_difference_expression(self, difference_expression):
        return '(DIFFERENCE-EXPRESSION : ' \
                f'{difference_expression.left.accept(self)}, ' \
                f'{difference_expression.right.accept(self)})'

    def visit_complement_expression(self, complement_expression):
        return '(COMPLEMENT-EXPRESSION : ' \
                f'{complement_expression.expression.accept(self)})'

    def visit_kleene_expression(self, kleene_expression):
        return '(KLEENE-EXPRESSION : ' \
                f'{kleene_expression.expression.accept(self)})'

    def visit_set(self, set):
        return '(SET : ' \
                f'{", ".join([ e.accept(self) for e in set.expressions ])})'

    def visit_symbol(self, symbol):
        return '(SYMBOL : ' \
                f'{symbol.identifier})'
    
    def visit_concatenate_expression(self, concatenate_expression):
        return '(CONCATENATION-EXPRESSION : ' \
                f'{concatenate_expression.left.accept(self)}, ' \
                f'{concatenate_expression.right.accept(self)})'

    def visit_string(self, string):
        if string.bits:
            return '(STRING : ' \
                    f'{string.bits if string.bits else "ε"})'
        else:
            return '(STRING : ε)'

def print_ast(ast):
    print(ASTStringifier().visit(ast))

class TypeChecker:

    class Type(enum.Enum):
        LANGUAGE = enum.auto()
        STRING   = enum.auto()
        
    def __init__(self):
        self.symbols = set()
        self.types = dict()

    def visit(self, node):
        if type(node) == Program:
            return self.visit_program(node)
        elif type(node) == LanguageDefinition:
            return self.visit_language_definition(node)
        elif type(node) == StringDefinition:
            return self.visit_string_definition(node)
        elif type(node) == ExclaimStatement:
            return self.visit_exclaim_statement(node)
        elif type(node) == InquireStatement:
            return self.visit_inquire_statement(node)
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
        elif type(node) == KleeneExpression:
            return self.visit_kleene_expression(node)
        elif type(node) == Set:
            return self.visit_set(node)
        elif type(node) == Symbol:
            return self.visit_symbol(node)
        elif type(node) == ConcatenateExpression:
            return self.visit_concatenate_expression(node)
        elif type(node) == String:
            return self.visit_string(node)
        raise RuntimeError('Unknown node type')

    def visit_program(self, program):
        for statement in program.statements:
            statement.accept(self)

    def visit_language_definition(self, language_definition):
        if language_definition.symbol in self.symbols:
            raise RuntimeError(f'Symbol "{language_definition.symbol.identifier}" defined twice')
        self.symbols.add(language_definition.symbol)
        self.types[language_definition.symbol] = TypeChecker.Type.LANGUAGE
        expression_type = language_definition.expression.accept(self)
        if expression_type != TypeChecker.Type.LANGUAGE:
            raise RuntimeError(f'LANGUAGE type expected, got {expression_type.name}')
            
    def visit_string_definition(self, string_definition):
        if string_definition.symbol in self.symbols:
            raise RuntimeError(f'Symbol "{string_definition.symbol.identifier}" defined twice')
        self.symbols.add(string_definition.symbol)
        self.types[string_definition.symbol] = TypeChecker.Type.STRING
        string_expression_type = string_definition.string_expression.accept(self)
        if string_expression_type != TypeChecker.Type.STRING:
            raise RuntimeError(f'STRING type expected, got {string_expression_type.name}')
        set_expression_type = string_definition.set_expression.accept(self)
        if set_expression_type != TypeChecker.Type.LANGUAGE:
            raise RuntimeError(f'LANGUAGE type expected, got {set_expression_type.name}')

    def visit_exclaim_statement(self, exclaim_statement):
        exclaim_statement.expression.accept(self)

    def visit_inquire_statement(self, inquire_statement):
        if inquire_statement.symbol in self.symbols:
            raise RuntimeError(f'Symbol "{inquire_statement.symbol.indentifier}" defined twice')
        self.symbols.add(inquire_statement.symbol)
        self.types[inquire_statement.symbol] = TypeChecker.Type.STRING
        expression_type = inquire_statement.expression.accept(self)
        if expression_type != TypeChecker.Type.LANGUAGE:
            raise RuntimeError(f'LANGUAGE type expected, got {expression_type.name}')

    def visit_union_expression(self, union_expression):
        left_type = union_expression.left.accept(self)
        if left_type != TypeChecker.Type.LANGUAGE:
            raise RuntimeError(f'LANGUAGE type expected, got {left_type.name}')
        right_type = union_expression.right.accept(self)
        if right_type != TypeChecker.Type.LANGUAGE:
            raise RuntimeError(f'LANGUAGE type expected, got {right_type.name}')
        return TypeChecker.Type.LANGUAGE

    def visit_intersect_expression(self, intersect_expression):
        left_type = intersect_expression.left.accept(self)
        if left_type != TypeChecker.Type.LANGUAGE:
            raise RuntimeError(f'LANGUAGE type expected, got {left_type.name}')
        right_type = intersect_expression.right.accept(self)
        if right_type != TypeChecker.Type.LANGUAGE:
            raise RuntimeError(f'LANGUAGE type expected, got {right_type.name}')
        return TypeChecker.Type.LANGUAGE

    def visit_product_expression(self, product_expression):
        left_type = product_expression.left.accept(self)
        if left_type != TypeChecker.Type.LANGUAGE:
            raise RuntimeError(f'LANGUAGE type expected, got {left_type.name}')
        right_type = product_expression.right.accept(self)
        if right_type != TypeChecker.Type.LANGUAGE:
            raise RuntimeError(f'LANGUAGE type expected, got {right_type.name}')
        return TypeChecker.Type.LANGUAGE
        
    def visit_difference_expression(self, difference_expression):
        left_type = difference_expression.left.accept(self)
        if left_type != TypeChecker.Type.LANGUAGE:
            raise RuntimeError(f'LANGUAGE type expected, got {left_type.name}')
        right_type = difference_expression.right.accept(self)
        if right_type != TypeChecker.Type.LANGUAGE:
            raise RuntimeError(f'LANGUAGE type expected, got {right_type.name}')
        return TypeChecker.Type.LANGUAGE
    
    def visit_complement_expression(self, complement_expression):
        expression_type = complement_expression.expression.accept(self)
        if expression_type != TypeChecker.Type.LANGUAGE:
            raise RuntimeError(f'LANGUAGE type expected, got {expression_type.name}')
        return TypeChecker.Type.LANGUAGE
    
    def visit_kleene_expression(self, kleene_expression):
        expression_type = kleene_expression.expression.accept(self)
        if expression_type != TypeChecker.Type.LANGUAGE:
            raise RuntimeError(f'LANGUAGE type expected, got {expression_type.name}')
        return TypeChecker.Type.LANGUAGE

    def visit_set(self, set):
        for expression in set.expressions:
            expression_type = expression.accept(self)
            if expression_type != TypeChecker.Type.STRING:
                raise RuntimeError(f'STRING type expected, got {expression_type.name}')
        return TypeChecker.Type.LANGUAGE

    def visit_symbol(self, symbol):
        if symbol not in self.symbols:
            raise RuntimeError(f'Symbol "{symbol.identifier}" not defined before use')
        return self.types[symbol]

    def visit_concatenate_expression(self, concatenate_expression):
        left_type = concatenate_expression.left.accept(self)
        if left_type != TypeChecker.Type.STRING:
            raise RuntimeError(f'STRING type expected, got {left_type.name}')
        right_type = concatenate_expression.right.accept(self)
        if right_type != TypeChecker.Type.STRING:
            raise RuntimeError(f'STRING type expected, got {right_type.name}')
        return TypeChecker.Type.STRING

    def visit_string(self, string):
        return TypeChecker.Type.STRING

def typecheck_ast(ast):
    TypeChecker().visit(ast)
