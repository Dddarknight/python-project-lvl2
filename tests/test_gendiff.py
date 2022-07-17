# -*- coding:utf-8 -*-


from gendiff.dict_diff import generate_diff


def make_set_txt_file(required_result):
    required_result_set = set()
    for line in required_result:
        line_corr = line.strip('\n')
        required_result_set.add(line_corr)
    return required_result_set


def make_set_func_res(func_result):
    func_result_set = set()
    func_result_corr = func_result.split('\n')
    for line in func_result_corr:
        func_result_set.add(line)
    return func_result_set


def test_gendiff_json_flat():
    required_result = open('tests/fixtures/result_flat.txt', 'r')
    func_result = generate_diff('tests/fixtures/file1.json', 'tests/fixtures/file2.json')
    assert make_set_func_res(func_result) == make_set_txt_file(required_result)


def test_gendiff_yaml_flat():
    required_result = open('tests/fixtures/result_flat.txt', 'r')
    func_result = generate_diff('tests/fixtures/file1.yaml', 'tests/fixtures/file2.yml')
    assert make_set_func_res(func_result) == make_set_txt_file(required_result)


def test_gendiff_json_yaml_flat():
    required_result = open('tests/fixtures/result_flat.txt', 'r')
    func_result = generate_diff('tests/fixtures/file1.json', 'tests/fixtures/file2.yml')
    assert make_set_func_res(func_result) == make_set_txt_file(required_result)


def test_gendiff_json_tree():
    required_result = open('tests/fixtures/result_tree.txt', 'r')
    func_result = generate_diff('tests/fixtures/file3.json', 'tests/fixtures/file4.json')
    assert make_set_func_res(func_result) == make_set_txt_file(required_result)


def test_gendiff_yaml_tree():
    required_result = open('tests/fixtures/result_tree.txt', 'r')
    func_result = generate_diff('tests/fixtures/file3.yaml', 'tests/fixtures/file4.yml')
    assert make_set_func_res(func_result) == make_set_txt_file(required_result)


def test_gendiff_json_yaml_tree():
    required_result = open('tests/fixtures/result_tree.txt', 'r')
    func_result = generate_diff('tests/fixtures/file3.json', 'tests/fixtures/file4.yml')
    assert make_set_func_res(func_result) == make_set_txt_file(required_result)


def test_gendiff_plain():
    required_result = open('tests/fixtures/result_plain.txt', 'r')
    func_result = generate_diff('tests/fixtures/file3.json', 'tests/fixtures/file4.yml', format_name='plain')
    assert make_set_func_res(func_result) == make_set_txt_file(required_result)


def make_set_txt_json(required_result):
    required_result_set = set()
    for line in required_result:
        required_line = ((str(line)).strip('\n')).strip(',')
        required_result_set.add(required_line)
    return required_result_set


def make_set_func_json(func_result):
    func_result_set = set()
    func_result_corr = func_result.split('\n')
    for line in func_result_corr:
        line_corr = line.strip(',')
        func_result_set.add(line_corr)
    return func_result_set


def test_gendiff_json_format():
    required_result = open('tests/fixtures/result_json_form.json', 'r')
    func_result = generate_diff('tests/fixtures/file3.json', 'tests/fixtures/file4.yml', format_name='json')
    assert make_set_func_json(func_result) == make_set_txt_json(required_result)
