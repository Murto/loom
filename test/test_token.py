#!/usr/bin/env python3

from loom import loomtoken
from loomtoken import TokenType, Symbol, Define, In, Union, Intersect, Product, Difference, Complement, LeftParenthesis, RightParenthesis, LeftBrace, RightBrace, EmptySet, Comma, String, tokenize
import os
import unittest

DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

class TestToken(unittest.TestCase):

    def test_spaced_tokens(self):
        EXPECTED = [
                Symbol('symbol'),
                Define(),
                In(),
                Union(),
                Intersect(),
                Product(),
                Difference(),
                Complement(),
                LeftParenthesis(),
                RightParenthesis(),
                LeftBrace(),
                RightBrace(),
                EmptySet(),
                Comma(),
                String(''),
                String('101010')
                ]
        FILE_PATH = os.path.join(DATA_PATH, 'spaced_tokens.lm')
        self.expect(EXPECTED, FILE_PATH)

    def test_unspaced_tokens(self):
        EXPECTED = [
                Symbol('symbol'),
                Define(),
                In(),
                Union(),
                Intersect(),
                Product(),
                Difference(),
                Complement(),
                LeftParenthesis(),
                RightParenthesis(),
                LeftBrace(),
                RightBrace(),
                EmptySet(),
                Comma(),
                String(''),
                String('101010')
                ]
        FILE_PATH = os.path.join(DATA_PATH, 'unspaced_tokens.lm')
        self.expect(EXPECTED, FILE_PATH)

    def expect(self, expected, file_path):
        with open(file_path) as source:
            for actual, expected in zip(tokenize(source.read()), expected):
                self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
