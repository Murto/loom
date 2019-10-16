#!/usr/bin/env python3

import argparse
import sys


def parse_arguments():
    description = 'loom is a toy language created by Murray Steele'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('source',
        metavar='source file', 
        type=str,
        help='loom language source file')
    args = parser.parse_args()
    return vars(args)
    
def main():
    arguments = parse_arguments()
    print(arguments)

if __name__ == '__main__':
    main()
