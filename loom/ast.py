#!/usr/bin/env python3

import abc

class AST(abc.ABC):
    pass

class Program:
    
    def __init__(self, alphabet_definitions, language_definitions, string_definitions):
        self._alphabet_definitions = list(alphabet_definitions)
        self._language_definitions = list(language_definitions)
        self._string_definitions = list(string_definitions)

class AlphabetDefinition(AST):

    def __init__(self, symbol, characters):
        self._symbol = symbol
        self._characters = characters

class LanguageDefinition(AST):

    def __init__(self, symbol, alphabet_symbol):
        self._symbol = symbol
        self._alphabet_symbol = alphabet_symbol

class StringDefinition(AST):
    
    def __init__(self, symbol, string, alphabet_symbol):
        self._symbol = symbol
        self._string = string
        self._alphabet_symbol = alphabet_symbol

