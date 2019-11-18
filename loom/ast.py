#!/usr/bin/env python3

import abc
import enum

class AST(abc.ABC):
    pass

class Program:
    
    def __init__(self, alphabet_definitions, language_definitions, string_definitions):
        self._alphabet_definitions = list(alphabet_definitions)
        self._language_definitions = list(language_definitions)
        self._string_definitions = list(string_definitions)

    def accept(self, visitor):
        visitor.visit(self)

class AlphabetDefinition(AST):

    def __init__(self, symbol, characters):
        self._symbol = symbol
        self._characters = characters

    def accept(self, visitor):
        visitor.visit(self)

class LanguageDefinition(AST):

    def __init__(self, symbol, alphabet_symbol):
        self._symbol = symbol
        self._alphabet_symbol = alphabet_symbol

    def accept(self, visitor):
        visitor.visit(self)

class StringDefinition(AST):
    
    def __init__(self, symbol, string, language_symbol):
        self._symbol = symbol
        self._string = string
        self._language_symbol = language_symbol

    def accept(self, visitor):
        visitor.visit(self)

class ASTPrinter:

    def visit(self, node):
        if type(node) == Program:
            self.__visit_program(node)
        elif type(node) == AlphabetDefinition:
            self.__visit_alphabet_definition(node)
        elif type(node) == LanguageDefinition:
            self.__visit_language_definition(node)
        elif type(node) == StringDefinition:
            self.__visit_string_definition(node)

    def __visit_program(self, program):
        print('(PROGRAM : ', end='')
        delim = ''
        for alphabet_definition in program._alphabet_definitions:
            print(delim, end='')
            alphabet_definition.accept(self)
            delim = ', '
        for language_definition in program._language_definitions:
            print(delim, end='')
            language_definition.accept(self)
            delim = ', '
        for string_definition in program._string_definitions:
            print(delim, end='')
            string_definition.accept(self)
            delim = ', '
        print(')')

    def __visit_alphabet_definition(self, alphabet_definition):
        print('(ALPHABET-DEFINITION : ', end='')
        print(alphabet_definition._symbol, end=', ')
        print(alphabet_definition._characters, end='')
        print(')', end='')

    def __visit_language_definition(self, language_definition):
        print('(LANGUAGE-DEFINITION : ', end='')
        print(language_definition._symbol, end=', ')
        print(language_definition._alphabet_symbol, end='*')
        print(')', end='')

    def __visit_string_definition(self, string_definition):
        print('(STRING-DEFINITION : ', end='')
        print(string_definition._symbol, end=', ')
        print(f'"{string_definition._string}"', end=', ')
        print(string_definition._language_symbol, end='*')
        print(')', end='')

class TypeChecker:

    def __init__(self):
        self.__symbols = set()
        self.__alphabets = set()
        self.__languages = set()
        self.__strings = set()

    def visit(self, node):
        if type(node) == Program:
            self.__visit_program(node)
        elif type(node) == AlphabetDefinition:
            self.__visit_alphabet_definition(node)
        elif type(node) == LanguageDefinition:
            self.__visit_language_definition(node)
        elif type(node) == StringDefinition:
            self.__visit_string_definition(node)

    def __visit_program(self, program):
        for alphabet_definition in program._alphabet_definitions:
            alphabet_definition.accept(self)
        for language_definition in program._language_definitions:
            language_definition.accept(self)
        for string_definition in program._string_definitions:
            string_definition.accept(self)

    def __visit_alphabet_definition(self, alphabet_definition):
        symbol = alphabet_definition._symbol
        if symbol in self.__symbols:
            raise RuntimeError('Symbol already declared')
        else:
            self.__symbols.add(symbol)
            self.__alphabets.add(symbol)
    
    def __visit_language_definition(self, language_definition):
        symbol = language_definition._symbol
        alphabet_symbol = language_definition._alphabet_symbol
        if symbol in self.__symbols:
            raise RuntimeError('Symbol already declared')
        elif alphabet_symbol not in self.__alphabets:
            raise RuntimeError('Alphabet not declared')
        else:
            self.__symbols.add(symbol)
            self.__languages.add(symbol)

    def __visit_string_definition(self, string_definition):
        symbol = string_definition._symbol
        language_symbol = string_definition._language_symbol
        if symbol in self.__symbols:
            raise RuntimeError('Symbol already declared')
        elif language_symbol not in self.__languages:
            raise RuntimeError('Language not declared')
        else:
            self.__symbols.add(symbol)
            self.__strings.add(symbol)
