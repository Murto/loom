#!/usr/bin/env python3

import loom
from loom import loomast, loomtoken, loomparse
from loomast import *
from loomparse import parse
from loomtoken import tokenize
import os
import unittest

DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

class TestParse(unittest.TestCase):

    def test_empty_parse(self):
        EXPECTED = Program([])
        FILE_PATH = os.path.join(DATA_PATH, 'empty_parse.lm')
        self.expect(EXPECTED, FILE_PATH)

    def test_language_definition(self):
        EXPECTED = Program([LanguageDefinition(Symbol('test'), Set([String('0101'), String('')]))])
        FILE_PATH = os.path.join(DATA_PATH, 'language_definition_parse.lm')
        self.expect(EXPECTED, FILE_PATH)

    def test_string_definition(self):
        EXPECTED = Program([StringDefinition(Symbol('test'), String('0101'), Symbol('test'))])
        FILE_PATH = os.path.join(DATA_PATH, 'string_definition_parse.lm')
        self.expect(EXPECTED, FILE_PATH)

    def test_program(self):
        EXPECTED = Program(                            \
            [LanguageDefinition(Symbol('strings'), ProductExpression(Set([String('0'), String('1')]), Set([String('0'), String('1')]))), \
            StringDefinition(Symbol('zero'), ConcatenateExpression(String('0'), String('0')), Symbol('strings'))])
        FILE_PATH = os.path.join(DATA_PATH, 'binary.lm')
        self.expect(EXPECTED, FILE_PATH)

    def expect(self, expected, file_path):
        with open(file_path) as source:
            tokens = list(tokenize(source.read()))
            actual = parse(tokens)
            self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()
