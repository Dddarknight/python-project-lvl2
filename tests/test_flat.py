# -*- coding:utf-8 -*-


from gendiff.generate import generate_diff


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
    required_result = open('tests/fixtures/result_json.txt', 'r')
    func_result = generate_diff('tests/fixtures/file1.json', 'tests/fixtures/file2.json')
    assert func_res(func_result) == txt_res(required_result)


def test_gendiff_yaml_flat():
    required_result = open('tests/fixtures/result_json.txt', 'r')
    func_result = generate_diff('tests/fixtures/file1.yaml', 'tests/fixtures/file2.yml')
    assert func_res(func_result) == txt_res(required_result)


def test_gendiff_json_yaml_flat():
    required_result = open('tests/fixtures/result_json.txt', 'r')
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
