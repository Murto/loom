#!/usr/bin/env python3

from loom import loomast, loomparse, loomtoken
from loomast import TypeChecker
from loomtoken import tokenize
from loomparse import parse
import os
import unittest

DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

class TestTupecheck(unittest.TestCase):

    def test_emptu_typecheck(self):
        FILE_PATH = os.path.join(DATA_PATH, 'empty_parse.lm')
        with open(FILE_PATH) as source:
            tokens = tokenize(source.read())
            tree = parse(tokens)
            try:
                TypeChecker().visit(tree)
            except RuntimeError:
                self.fail('TypeChecker raised error unexpectedly')

    def test_emptu_typecheck(self):
        FILE_PATH = os.path.join(DATA_PATH, 'alphabet_definition_parse.lm')
        with open(FILE_PATH) as source:
            tokens = tokenize(source.read())
            tree = parse(tokens)
            try:
                TypeChecker().visit(tree)
            except RuntimeError:
                self.fail('TypeChecker raised error unexpectedly')

    def test_emptu_typecheck(self):
        FILE_PATH = os.path.join(DATA_PATH, 'language_definition_parse.lm')
        with open(FILE_PATH) as source:
            tokens = tokenize(source.read())
            tree = parse(tokens)
            try:
                TypeChecker().visit(tree)
            except RuntimeError:
                self.fail('TypeChecker raised error unexpectedly')

    def test_emptu_typecheck(self):
        FILE_PATH = os.path.join(DATA_PATH, 'string_definition_parse.lm')
        with open(FILE_PATH) as source:
            tokens = tokenize(source.read())
            tree = parse(tokens)
            try:
                TypeChecker().visit(tree)
            except RuntimeError:
                self.fail('TypeChecker raised error unexpectedly')
