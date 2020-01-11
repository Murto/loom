#!/usr/bin/env python3

import abc
from functools import partial
from loomast import *

class ProgramGenerator:

    def __init__(self):
        self.string_count = 0
        self.set_count = 0
        self.program = []
        self.environment = dict()

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
        return '\n'.join(self.program)

    def visit_language_definition(self, language_definition):
        variable = language_definition.expression.accept(self)
        self.environment[language_definition.symbol.identifier] = variable

    def visit_string_definition(self, string_definition):
        variable = string_definition.string_expression.accept(self)
        self.environment[string_definition.symbol.identifier] = variable
        predicate = string_definition.set_expression.accept(self)
        self.program.append(f'assert {predicate}({variable}), "String does not satisfy predicate"')

    def visit_exclaim_statement(self, exclaim_statement):
        local = exclaim_statement.expression.accept(self)
        self.program.append(f'print({local})')

    def visit_inquire_statement(self, inquire_statement):
        local = self.next_string()
        self.environment[inquire_statement.symbol.identifier] = local
        predicate = inquire_statement.expression.accept(self)
        self.program.append(f'{local} = input()')
        self.program.append(f'assert all(x in "01" for x in {local}), "Input string is not binary"')
        self.program.append(f'assert {predicate}({local}), "String does not satisfy predicate"')

    def visit_union_expression(self, union_expression):
        left_argument = union_expression.left.accept(self)
        right_argument = union_expression.right.accept(self)
        variable = self.next_set()
        self.program.append(f'{variable} = lambda item: {left_argument}(item) or {right_argument}(item)')
        return variable

    def visit_intersect_expression(self, intersect_expression):
        left_argument = intersect_expression.left.accept(self)
        right_argument = intersect_expression.right.accept(self)
        variable = self.next_set()
        self.program.append(f'{variable} = lambda item: {left_argument}(left) and {right_argument}(item)')
        return variable

    def visit_product_expression(self, product_expression):
        left_argument = product_expression.left.accept(self)
        right_argument = product_expression.right.accept(self)
        variable = self.next_set()
        self.program.append(f'{variable} = lambda item: any({left_argument}(item[:i]) and {right_argument}(item[i:]) for i in range(len(item) + 1))')
        return variable

    def visit_difference_expression(self, difference_expression):
        left_argument = difference_expression.left.accept(self)
        right_argument = difference_expression.right.accept(self)
        variable = self.next_set()
        self.program.append(f'{variable} = lambda item: {left_argument}(item) and not {right_argument}(item)')
        return variable

    def visit_complement_expression(self, complement_expression):
        argument = complement_expression.expression.accept(self)
        variable = self.next_set()
        self.program.append(f'{variable} = lambda item: not {argument}(item)')
        return variable

    def visit_set(self, set):
        variables = []
        for expression in set.expressions:
            variables.append(expression.accept(self))
        variable = self.next_set()
        self.program.append(f'{variable} = lambda item: item in [{",".join(variables)}]')
        return variable

    def visit_symbol(self, symbol):
        return self.environment[symbol.identifier]

    def visit_concatenate_expression(self, concatenate_expression):
        left_argument = concatenate_expression.left.accept(self)
        right_argument = concatenate_expression.right.accept(self)
        variable = self.next_string()
        self.program.append(f'{variable} = {left_argument} + {right_argument}')
        return variable

    def visit_string(self, string):
        variable = self.next_string()
        self.program.append(f'{variable} = "{string.bits}"')
        return variable

    def next_string(self):
        variable = 'string_' + str(self.string_count)
        self.string_count += 1
        return variable

    def next_set(self):
        variable = 'set_' + str(self.set_count)
        self.set_count += 1
        return variable

def generate_program(ast):
    return ProgramGenerator().visit(ast)
