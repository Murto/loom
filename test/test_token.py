#!/usr/bin/env python3

import loom
from loom.token import TokenType, tokenize
import os
import unittest

DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

class TestToken(unittest.TestCase):

    def test_spaced_tokens(self):
        EXPECTED = [
                (TokenType.LET, 'let'),
                (TokenType.ASSIGN, '='),
                (TokenType.LEFT_BRACE, '{'),
                (TokenType.RIGHT_BRACE, '}'),
                (TokenType.ASTERISK, '*'),
                (TokenType.IN, 'in'),
                (TokenType.COMMA, ','),
                (TokenType.SYMBOL, 'symbol'),
                (TokenType.CHARACTER, '\'a\''),
                (TokenType.STRING, '"string"'),
                (TokenType.NEWLINE, '\n')
                ]
        FILE_PATH = os.path.join(DATA_PATH, 'spaced_tokens.lm')
        with open(FILE_PATH) as source:
            for token, expected in zip(tokenize(source.read()), EXPECTED):
                actual = (token.type, token.value)
                self.assertEqual(actual, expected)

    def test_unspaced_tokens(self):
        EXPECTED = [
                (TokenType.LET, 'let'),
                (TokenType.ASSIGN, '='),
                (TokenType.LEFT_BRACE, '{'),
                (TokenType.RIGHT_BRACE, '}'),
                (TokenType.ASTERISK, '*'),
                (TokenType.IN, 'in'),
                (TokenType.COMMA, ','),
                (TokenType.SYMBOL, 'symbol'),
                (TokenType.CHARACTER, '\'a\''),
                (TokenType.STRING, '"string"'),
                (TokenType.NEWLINE, '\n')
                ]
        FILE_PATH = os.path.join(DATA_PATH, 'unspaced_tokens.lm')
        with open(FILE_PATH) as source:
            for token, expected in zip(tokenize(source.read()), EXPECTED):
                actual = (token.type, token.value)
                self.assertEqual(actual, expected)

    def test_invalid_tokens(self):
        FILE_PATH = os.path.join(DATA_PATH, 'invalid_tokens.lm')
        with open(FILE_PATH) as source:
            self.assertRaises(RuntimeError, tokenize, source.read())


if __name__ == '__main__':
    unittest.main()