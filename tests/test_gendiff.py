# -*- coding:utf-8 -*-


import pytest
import os
import sys
from gendiff import generate_diff
from gendiff.parsers.cli_parsing import parse
from unittest import mock


def get_fixture_path(name):
    return os.path.join('tests/fixtures', name)


@pytest.mark.parametrize(
    'result_file_name, file1_name, file2_name, formatter_name',
    [('result.flat', 'file1.json', 'file2.json', 'stylish'),
     ('result.flat', 'file1.yaml', 'file2.yml', 'stylish'),
     ('result.flat', 'file1.json', 'file2.yml', 'stylish'),
     ('result.tree', 'file3.json', 'file4.json', 'stylish'),
     ('result.tree', 'file3.yaml', 'file4.yml', 'stylish'),
     ('result.tree', 'file3.json', 'file4.yml', 'stylish'),
     ('result.plain', 'file3.json', 'file4.yml', 'plain'),
     ('result.plain', 'file3.json', 'file4.json', 'plain'),
     ('result.json', 'file3.json', 'file4.yml', 'json'),
     ('result.json', 'file3.json', 'file4.json', 'json')])
def test_gendiff(result_file_name, file1_name, file2_name, formatter_name):
    with open(get_fixture_path(result_file_name), 'r') as read_file:
        required_result = read_file.read()
    func_result = generate_diff(get_fixture_path(file1_name),
                                get_fixture_path(file2_name),
                                formatter_name)
    assert func_result == required_result


def test_default_in_parser():
    sys.argv.append('/dir/file1')
    sys.argv.append('/dir/file2')
    parser_args = parse()
    print(parser_args)
    assert parser_args['format'] == 'stylish'
