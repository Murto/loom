#!/usr/bin/env python3

from copy import deepcopy
import loomast
import loomtoken
from loomtoken import TokenType

def lookahead(tokens, *expected):
    seen = all([ type(token) == expected_type for (token, expected_type) in zip(tokens, expected) ])
    if not seen:
        return [], tokens
    return tokens[:len(expected)], tokens[len(expected):]

def parse(tokens):
    next_tokens = deepcopy(tokens)
    statements, next_tokens = parse_statements(next_tokens)
    if not statements:
        statements = []
    next_tokens = parse_newlines(next_tokens)
    if next_tokens:
        raise RuntimeError(f'Unexpected token {next_tokens[0]}')
    return loomast.Program(statements)

def parse_statements(tokens):
    next_tokens = deepcopy(tokens)
    statements = []
    statement, next_tokens = parse_statement(next_tokens)
    while statement:
        statements.append(statement)
        statement, next_tokens = parse_statement(next_tokens)
    return statements, next_tokens

def parse_statement(tokens):
    next_tokens = deepcopy(tokens)
    language_definition, next_tokens = parse_language_definition(next_tokens)
    if language_definition:
        return language_definition, next_tokens
    string_definition, next_tokens = parse_string_definition(next_tokens)
    if string_definition:
        return string_definition, next_tokens
    return None, tokens

def parse_language_definition(tokens):
    next_tokens = deepcopy(tokens)
    seen, next_tokens = lookahead(next_tokens, loomtoken.Symbol, loomtoken.Define)
    if not seen:
        return None, tokens
    symbol = loomast.Symbol(seen[0].identifier)
    expression, next_tokens = parse_set_expression(next_tokens)
    if not expression:
        return None, tokens
    seen, next_tokens = lookahead(next_tokens, loomtoken.Newline)
    if not seen:
        return None, tokens
    return loomast.LanguageDefinition(symbol, expression), next_tokens

def parse_string_definition(tokens):
    next_tokens = deepcopy(tokens)
    seen, next_tokens = lookahead(next_tokens, loomtoken.Symbol, loomtoken.Define)
    if not seen:
        return None, tokens
    symbol = loomast.Symbol(seen[0].identifier)
    string_expression, next_tokens = parse_string_expression(next_tokens)
    if not string_expression:
        return None, tokens
    seen, next_tokens = lookahead(next_tokens, loomtoken.In)
    if not seen:
        return None, tokens
    set_expression, next_tokens = parse_set_expression(next_tokens)
    if not set_expression:
        return None, tokens
    seen, next_tokens = lookahead(next_tokens, loomtoken.Newline)
    if not seen:
        return None, tokens
    return loomast.StringDefinition(symbol, string_expression, set_expression), next_tokens

def parse_set_expression(tokens):
    next_tokens = deepcopy(tokens)
    return parse_union_expression(next_tokens)

def parse_union_expression(tokens):
    next_tokens = deepcopy(tokens)
    left_expression, next_tokens = parse_intersect_expression(next_tokens)
    if not left_expression:
        return None, tokens
    seen, next_tokens = lookahead(next_tokens, loomtoken.Union)
    if not seen:
        return left_expression, next_tokens
    right_expression, next_tokens = parse_union_expression(next_tokens)
    if not right_expression:
        return None, tokens
    return loomast.UnionExpression(left_expression, right_expression), next_tokens

def parse_intersect_expression(tokens):
    next_tokens = deepcopy(tokens)
    left_expression, next_tokens = parse_product_expression(next_tokens)
    if not left_expression:
        return None, tokens
    seen, next_tokens = lookahead(next_tokens, loomtoken.Intersect)
    if not seen:
        return left_expression, next_tokens
    right_expression, next_tokens = parse_intersect_expression(next_tokens)
    if not right_expression:
        return None, tokens
    return loomast.IntersectExpression(left_expression, right_expression), next_tokens

def parse_product_expression(tokens):
    next_tokens = deepcopy(tokens)
    left_expression, next_tokens = parse_difference_expression(next_tokens)
    if not left_expression:
        return None, tokens
    seen, next_tokens = lookahead(next_tokens, loomtoken.Product)
    if not seen:
        return left_expression, next_tokens
    right_expression, next_tokens = parse_product_expression(next_tokens)
    if not right_expression:
        return None, tokens
    return loomast.ProductExpression(left_expression, right_expression), next_tokens

def parse_difference_expression(tokens):
    next_tokens = deepcopy(tokens)
    left_expression, next_tokens = parse_complement_expression(next_tokens)
    if not left_expression:
        return None, tokens
    seen, next_tokens = lookahead(next_tokens, loomtoken.Difference)
    if not seen:
        return left_expression, next_tokens
    right_expression, next_tokens = parse_difference_expression(next_tokens)
    if not right_expression:
        return None, tokens
    return loomast.DifferenceExpression(left_expression, right_expression), next_tokens

def parse_complement_expression(tokens):
    next_tokens = deepcopy(tokens)
    seen, next_tokens = lookahead(next_tokens, loomtoken.Complement)
    if seen:
        return loomast.Complement(parse_complement_expression(next_tokens)), next_tokens
    return parse_set_parenthesis_expression(next_tokens)

def parse_set_parenthesis_expression(tokens):
    next_tokens = deepcopy(tokens)
    seen, next_tokens = lookahead(next_tokens, loomtoken.LeftParenthesis)
    if seen:
        expression, next_tokens = parse_set_expression(next_tokens)
        seen, next_tokens = lookahead(next_tokens, loomtoken.RightParenthesis)
        if not seen:
            return None, tokens
        return expression, next_tokens
    set, next_tokens = parse_set(next_tokens)
    if set:
        return set, next_tokens
    seen, next_tokens = lookahead(next_tokens, loomtoken.Symbol)
    if seen:
        return loomast.Symbol(seen[0].identifier), next_tokens
    return None, tokens

def parse_set(tokens):
    next_tokens = deepcopy(tokens)
    seen, next_tokens = lookahead(next_tokens, loomtoken.LeftBrace)
    if seen:
        expressions, next_tokens = parse_string_expression_list(next_tokens)
        if not expressions:
            return None, tokens
        seen, next_tokens = lookahead(next_tokens, loomtoken.RightBrace)
        if not seen:
            return None, tokens
        return loomast.Set(expressions), next_tokens
    seen, next_tokens = lookahead(next_tokens, loomtoken.EmptySet)
    if not seen:
        return None, tokens
    return loomast.Set([]), next_tokens

def parse_string_expression(tokens):
    next_tokens = deepcopy(tokens)
    return parse_concatenate_expression(next_tokens)

def parse_concatenate_expression(tokens):
    next_tokens = deepcopy(tokens)
    left_expression, next_tokens = parse_string_parenthesis_expression(next_tokens)
    if not left_expression:
        return None, tokens
    seen, next_tokens = lookahead(next_tokens, loomtoken.Concatenate)
    if not seen:
        return left_expression, next_tokens
    right_expression, next_tokens = parse_string_parenthesis_expression(next_tokens)
    if not right_expression:
        return None, tokens
    return loomast.ConcatenateExpression(left_expression, right_expression), next_tokens

def parse_string_parenthesis_expression(tokens):
    next_tokens = deepcopy(tokens)
    seen, next_tokens = lookahead(next_tokens, loomtoken.LeftParenthesis)
    if seen:
        expression, next_tokens = parse_string_expression(next_tokens)
        if not expression:
            return None, tokens
        seen, next_tokens = lookahead(next_tokens, loomtoken.RightParenthesis)
        if not seen:
            return None, tokens
        return expression, next_tokens
    seen, next_tokens = lookahead(next_tokens, loomtoken.String)
    if seen:
        return loomast.String(seen[0].bits), next_tokens
    seen, next_tokens = lookahead(next_tokens, loomtoken.Symbol)
    if seen:
        return loomast.Symbol(seen[0].identifier), next_tokens
    return None, tokens

def parse_string_expression_list(tokens):
    next_tokens = deepcopy(tokens)
    expressions = []
    expression, next_tokens = parse_string_expression(next_tokens)
    if not expression:
        return None, tokens
    expressions.append(expression)
    seen, next_tokens = lookahead(next_tokens, loomtoken.Comma)
    while seen:
        expression, next_tokens = parse_string_expression(next_tokens)
        if not expression:
            return None, tokens
        expressions.append(expression)
        seen, next_tokens = lookahead(next_tokens, loomtoken.Comma)
    return expressions, next_tokens

def parse_newlines(tokens):
    next_tokens = deepcopy(tokens)
    seen, next_tokens = lookahead(next_tokens, loomtoken.Newline)
    while seen:
        seen, tokens = lookahead(next_tokens, loomtoken.Newline)
    return tokens
