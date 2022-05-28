# -*- coding:utf-8 -*-


from gendiff.generate import generate_diff


def test_gendiff_json():
    required_result_set, func_result_set = set(), set()
    required_result = open('tests/fixtures/result_json.txt', 'r')
    func_result = generate_diff('tests/fixtures/file1.json', 'tests/fixtures/file2.json')
    func_result_corr = func_result.split('\n')
    for line in required_result:
        required_result_set.add(line)
    for index, line in enumerate(func_result_corr):
        if index == len(func_result_corr) - 1:
            line_corr = line
        else:
            line_corr = line + '\n'
        func_result_set.add(line_corr)
    assert func_result_set == required_result_set


def test_gendiff_yaml():
    required_result_set, func_result_set = set(), set()
    required_result = open('tests/fixtures/result_json.txt', 'r')
    func_result = generate_diff('tests/fixtures/file1.yaml', 'tests/fixtures/file2.yml')
    func_result_corr = func_result.split('\n')
    for line in required_result:
        required_result_set.add(line)
    for index, line in enumerate(func_result_corr):
        if index == len(func_result_corr) - 1:
            line_corr = line
        else:
            line_corr = line + '\n'
        func_result_set.add(line_corr)
    print(func_result_set)
    assert func_result_set == required_result_set


def test_gendiff_json_yaml():
    required_result_set, func_result_set = set(), set()
    required_result = open('tests/fixtures/result_json.txt', 'r')
    func_result = generate_diff('tests/fixtures/file1.json', 'tests/fixtures/file2.yml')
    func_result_corr = func_result.split('\n')
    for line in required_result:
        required_result_set.add(line)
    for index, line in enumerate(func_result_corr):
        if index == len(func_result_corr) - 1:
            line_corr = line
        else:
            line_corr = line + '\n'
        func_result_set.add(line_corr)
    assert func_result_set == required_result_set
