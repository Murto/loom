#!/usr/bin/env python3

from loom import loomast, loomparse, loomtoken
from loomast import typecheck_ast
from loomtoken import tokenize
from loomparse import parse
import os
import unittest

DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

class TestTupecheck(unittest.TestCase):

    def test_emptu_typecheck(self):
        FILE_PATH = os.path.join(DATA_PATH, 'empty_parse.lm')
        self.typecheck(FILE_PATH)

    def test_language_typecheck(self):
        FILE_PATH = os.path.join(DATA_PATH, 'language_definition_typecheck.lm')
        self.typecheck(FILE_PATH)

    def test_string_typecheck(self):
        FILE_PATH = os.path.join(DATA_PATH, 'string_definition_typecheck.lm')
        self.typecheck(FILE_PATH)
    
    def typecheck(self, file_path):
        with open(file_path) as source:
            tokens = list(tokenize(source.read()))
            tree = parse(tokens)
            try:
                typecheck_ast(tree)
            except RuntimeError:
                self.fail('TypeChecker raised error unexpectedly')
