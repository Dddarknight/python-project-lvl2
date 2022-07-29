import gendiff.formatters.stylish as stylish
import gendiff.formatters.plain as plain
import gendiff.formatters.json as json_format
from gendiff.diffs import tree
from gendiff.converters import file_to_dict


MAP_INPUT_TO_FORMATTER = {'stylish': stylish,
                          'plain': plain,
                          'json': json_format}


def generate_diff(file1_path, file2_path, formatter_name='stylish'):
    file1_dict = file_to_dict.convert(file1_path)
    file2_dict = file_to_dict.convert(file2_path)
    diff = tree.make(file1_dict, file2_dict)
    formatter = MAP_INPUT_TO_FORMATTER[formatter_name]
    return formatter.modify(diff, file1_dict, file2_dict)
