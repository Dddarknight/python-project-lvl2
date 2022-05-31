# -*- coding:utf-8 -*-


from gendiff.generate import generate_diff
import json


def txt_res(required_result):
    required_result_set = set()
    for line in required_result:
        required_result_set.add(line)
    return required_result_set


def func_res(func_result):
    func_result_set = set()
    func_result_corr = func_result.split('\n')
    for index, line in enumerate(func_result_corr):
        if index == len(func_result_corr) - 1:
            line_corr = line
        else:
            line_corr = line + '\n'
        func_result_set.add(line_corr)
    return func_result_set

def test_gendiff_json_flat():
    required_result = open('tests/fixtures/result_flat.txt', 'r')
    func_result = generate_diff('tests/fixtures/file1.json', 'tests/fixtures/file2.json')
    assert func_res(func_result) == txt_res(required_result)


def test_gendiff_yaml_flat():
    required_result = open('tests/fixtures/result_flat.txt', 'r')
    func_result = generate_diff('tests/fixtures/file1.yaml', 'tests/fixtures/file2.yml')
    assert func_res(func_result) == txt_res(required_result)


def test_gendiff_json_yaml_flat():
    required_result = open('tests/fixtures/result_flat.txt', 'r')
    func_result = generate_diff('tests/fixtures/file1.json', 'tests/fixtures/file2.yml')
    assert func_res(func_result) == txt_res(required_result)


def test_gendiff_json_tree():
    required_result = open('tests/fixtures/result_tree.txt', 'r')
    func_result = generate_diff('tests/fixtures/file3.json', 'tests/fixtures/file4.json')
    assert func_res(func_result) == txt_res(required_result)


def test_gendiff_yaml_tree():
    required_result = open('tests/fixtures/result_tree.txt', 'r')
    func_result = generate_diff('tests/fixtures/file3.yaml', 'tests/fixtures/file4.yml')
    assert func_res(func_result) == txt_res(required_result)


def test_gendiff_json_yaml_tree():
    required_result = open('tests/fixtures/result_tree.txt', 'r')
    func_result = generate_diff('tests/fixtures/file3.json', 'tests/fixtures/file4.yml')
    assert func_res(func_result) == txt_res(required_result)


def test_gendiff_plain():
    required_result = open('tests/fixtures/result_plain.txt', 'r')
    func_result = generate_diff('tests/fixtures/file3.json', 'tests/fixtures/file4.yml', format_name='plain')
    assert func_res(func_result) == txt_res(required_result)


def txt_res_json_form(required_result):
    required_result_set = set()
    for line in required_result:
        required_line = ((str(line)).strip('\n')).strip(',')
        required_result_set.add(required_line)
    return required_result_set


def func_res_json_form(func_result):
    func_result_set = set()
    func_result_corr = func_result.split('\n')
    for line in func_result_corr:
        line_corr = line.strip(',')
        func_result_set.add(line_corr)
    return func_result_set


def test_gendiff_json_format():
    required_result = open('tests/fixtures/result_json_form.json', 'r')
    func_result = generate_diff('tests/fixtures/file3.json', 'tests/fixtures/file4.yml', format_name='json')
    assert func_res_json_form(func_result) == txt_res_json_form(required_result)