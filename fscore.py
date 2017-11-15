#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys


def main(test, result):
    pass


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python fscore.py testfile resultfile")
        sys.exit()
    test_file = sys.argv[1]
    result_file = sys.argv[2]
    main(test_file, result_file)