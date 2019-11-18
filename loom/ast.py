#!/usr/bin/env python3

import abc

class AST(abc.ABC):
    pass

class Program:
    
    def __init__(self, alphabet_definitions, language_definitions, string_definitions):
        self.__alphabet_definitions = list(alphabet_definitions)
        self.__language_definitions = list(language_definitions)
        self.__string_definitions = list(string_definitions)

class AlphabetDefinition(AST):

    def __init__(self, symbol, characters):
        self.__symbol = symbol
        self.__characters = characters

class LanguageDefinition(AST):

    def __init__(self, symbol, alphabet_symbol):
        self.__symbol = symbol
        self.__alphabet_symbol = alphabet_symbol

class StringDefinition(AST):
    
    def __init__(self, symbol, string, alphabet_symbol):
        self.__symbol = symbol
        self.__string = string
        self.__alphabet_symbol = alphabet_symbol

