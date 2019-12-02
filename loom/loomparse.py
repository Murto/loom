#!/usr/bin/env python3

import loomast
import loomtoken
from loomast import Program, AlphabetDefinition, LanguageDefinition, StringDefinition, String
from loomtoken import Token, TokenType

def lookahead(tokens, *expected):
    seen = all([ token.type == type for (token, type) in zip(tokens, expected) ])
    if seen:
        return tokens[:len(expected)], tokens[len(expected):]
    else:
        return [], tokens

def parse(tokens):
    alphabet_definitions, tokens = parse_alphabet_definitions(tokens)
    language_definitions, tokens = parse_language_definitions(tokens)
    string_definitions, tokens = parse_string_definitions(tokens)
    tokens = parse_newlines(tokens)
    if tokens:
        raise RuntimeError(f'Unexpected token {tokens[0].type}')
    else:
        return Program(alphabet_definitions, language_definitions, string_definitions)

def parse_alphabet_definitions(tokens):
    alphabet_definitions = list()
    alphabet_definition, tokens = parse_alphabet_definition(tokens)
    while alphabet_definition:
        alphabet_definitions.append(alphabet_definition)
        alphabet_definition, tokens = parse_alphabet_definition(tokens)
    return alphabet_definitions, tokens

def parse_alphabet_definition(tokens):
    seen, tokens = lookahead(tokens, TokenType.LET, TokenType.SYMBOL, TokenType.ASSIGN, TokenType.LEFT_BRACE)
    if seen:
        symbol = seen[1].value
        symbol_list, tokens = parse_symbol_list(tokens)
        seen, tokens = lookahead(tokens, TokenType.RIGHT_BRACE, TokenType.NEWLINE)
        if seen:
            return AlphabetDefinition(symbol, symbol_list), tokens
        else:
            return None, tokens
    else:
        return None, tokens

def parse_symbol_list(tokens):
    seen, tokens = lookahead(tokens, TokenType.SYMBOL)
    if seen:
        symbols = [seen[0].value]
        seen, tokens = lookahead(tokens, TokenType.COMMA, TokenType.SYMBOL)
        while seen:
            symbols.append(seen[1].value)
            seen, tokens = lookahead(tokens, TokenType.COMMA, TokenType.SYMBOL)
        return symbols, tokens
    else:
        return [], tokens

def parse_language_definitions(tokens):
    language_definitions = list()
    language_definition, tokens = parse_language_definition(tokens)
    while language_definition:
        language_definitions.append(language_definition)
        language_definition, tokens = parse_language_definition(tokens)
    return language_definitions, tokens

def parse_language_definition(tokens):
    seen, tokens = lookahead(tokens, TokenType.LET, TokenType.SYMBOL, TokenType.ASSIGN, TokenType.SYMBOL, TokenType.ASTERISK, TokenType.NEWLINE)
    if seen:
        return LanguageDefinition(seen[1].value, seen[3].value), tokens
    else:
        return None, tokens

def parse_string_definitions(tokens):
    string_definitions = list()
    string_definition, tokens = parse_string_definition(tokens)
    while string_definition:
        string_definitions.append(string_definition)
        string_definition, tokens = parse_string_definition(tokens)
    return string_definitions, tokens

def parse_string_definition(tokens):
    seen, tokens = lookahead(tokens, TokenType.LET, TokenType.SYMBOL, TokenType.ASSIGN)
    if seen:
        symbol = seen[1].value
        string, tokens = parse_string(tokens)
        if string:
            seen, tokens = lookahead(tokens, TokenType.IN, TokenType.SYMBOL, TokenType.NEWLINE)
            if seen:
                alphabet_symbol = seen[1].value
                return StringDefinition(symbol, string, alphabet_symbol), tokens
            else:
                return None, tokens
        else:
            return None, tokens
    else:
        return None, tokens

def parse_string(tokens):
    seen, tokens = lookahead(tokens, TokenType.LEFT_BRACKET)
    if seen:
        symbols, tokens = parse_symbol_list(tokens)
        seen, tokens = lookahead(tokens, TokenType.RIGHT_BRACKET)
        if seen:
            return String(symbols), tokens
        else:
            return None, tokens
    else:
        return None, tokens

def parse_newlines(tokens):
    seen, tokens = lookahead(tokens, TokenType.NEWLINE)
    while seen:
        seen, tokens = lookahead(tokens, TokenType.NEWLINE)
    return tokens
