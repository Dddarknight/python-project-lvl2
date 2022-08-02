import gendiff.formatters.stylish as stylish
import gendiff.formatters.plain as plain
import gendiff.formatters.json as json_format


MAP_INPUT_TO_FORMATTER = {'stylish': stylish,
                          'plain': plain,
                          'json': json_format}


def modify(diff, file1_dict, file2_dict, formatter_name):
    formatter = MAP_INPUT_TO_FORMATTER[formatter_name]
    return formatter.modify(diff, file1_dict, file2_dict)
