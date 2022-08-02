# -*- coding:utf-8 -*-


import pytest
import os
from gendiff import generate_diff


FORMATS = ['json', 'yml', 'yaml']


def get_fixture_path(name):
    return os.path.join('tests/fixtures', name)


@pytest.mark.parametrize(
    'result_file_name, file1_name, file2_name, formatter_name',
    [('result.flat', 'file1', 'file2', 'stylish'),
     ('result.tree', 'file3', 'file4', 'stylish'),
     ('result.plain', 'file3', 'file4', 'plain'),
     ('result.json', 'file3', 'file4', 'json')])
def test_gendiff(result_file_name, file1_name, file2_name, formatter_name):
    with open(get_fixture_path(result_file_name), 'r') as read_file:
        required_result = read_file.read()
    for file1_format in FORMATS:
        for file2_format in FORMATS:
            file1_path = f'{get_fixture_path(file1_name)}.{file1_format}'
            file2_path = f'{get_fixture_path(file2_name)}.{file2_format}'
            result = generate_diff(file1_path, file2_path, formatter_name)
            assert result == required_result


@pytest.mark.parametrize(
    'file1_name, file2_name',
    [('file1', 'file2'),
     ('file3', 'file4')])
def test_default_format(file1_name, file2_name):
    for file1_format in FORMATS:
        for file2_format in FORMATS:
            file1_path = f'{get_fixture_path(file1_name)}.{file1_format}'
            file2_path = f'{get_fixture_path(file2_name)}.{file2_format}'
            result_with_default = generate_diff(file1_path, file2_path)
            result_with_stylish = generate_diff(
                file1_path, file2_path, formatter_name='stylish')
            assert result_with_default == result_with_stylish
