#!/usr/bin/env python

from gendiff.generate import generate_diff
from gendiff.parsing import parsing


def main():
    args = parsing()
    print(generate_diff(args['first_file'], args['second_file']))


if __name__ == '__main__':
    main()
