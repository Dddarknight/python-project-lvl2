# -*- coding:utf-8 -*-


from gendiff.generate import generate_diff


def test_gendiff():
    required_result_set, func_result_set = set(), set()
    required_result = open('tests/result_json.txt', 'r')
    func_result = generate_diff('tests/file1.json', 'tests/file2.json')
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
