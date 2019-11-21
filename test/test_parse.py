#!/usr/bin/env python3

import loom
from loom import loomast, loomtoken, loomparse
from loomast import Program, AlphabetDefinition, LanguageDefinition, StringDefinition
from loomparse import parse
from loomtoken import tokenize
import os
import unittest

DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

class TestParse(unittest.TestCase):

    def test_empty_parse(self):
        EXPECTED = Program([], [], [])
        FILE_PATH = os.path.join(DATA_PATH, 'empty_parse.lm')
        with open(FILE_PATH) as source:
            tokens = tokenize(source.read())
            actual = parse(tokens)
            self.assertEqual(actual, EXPECTED)

    def test_alphabet_definition(self):
        EXPECTED = Program([AlphabetDefinition('test', ['0', '1'])], [], [])
        FILE_PATH = os.path.join(DATA_PATH, 'alphabet_definition_parse.lm')
        with open(FILE_PATH) as source:
            tokens = tokenize(source.read())
            actual = parse(tokens)
            self.assertEqual(actual, EXPECTED)

    def test_language_definition(self):
        EXPECTED = Program([], [LanguageDefinition('test', 'test')], [])
        FILE_PATH = os.path.join(DATA_PATH, 'language_definition_parse.lm')
        with open(FILE_PATH) as source:
            tokens = tokenize(source.read())
            actual = parse(tokens)
            self.assertEqual(actual, EXPECTED)

    def test_string_definition(self):
        EXPECTED = Program([], [], [StringDefinition('test', 'test', 'test')])
        FILE_PATH = os.path.join(DATA_PATH, 'string_definition_parse.lm')
        with open(FILE_PATH) as source:
            tokens = tokenize(source.read())
            actual = parse(tokens)
            self.assertEqual(actual, EXPECTED)

    def test_program(self):
        EXPECTED = Program(                            \
            [AlphabetDefinition('binary', ['0', '1'])],\
            [LanguageDefinition('strings', 'binary')], \
            [StringDefinition('zero', '0', 'strings')])
        FILE_PATH = os.path.join(DATA_PATH, 'binary.lm')
        with open(FILE_PATH) as source:
            tokens = tokenize(source.read())
            actual = parse(tokens)
            self.assertEqual(actual, EXPECTED)
