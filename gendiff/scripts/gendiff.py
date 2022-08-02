#!/usr/bin/env python

from gendiff import generate_diff
from gendiff.parsers.cli import parse


def main():
    args = parse()
    print(generate_diff(
        args.first_file, args.second_file, formatter_name=args.format))


if __name__ == '__main__':
    main()
