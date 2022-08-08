import json
import yaml


def convert(file_data, file_format):
    if file_format == 'json':
        return json.load(file_data)
    elif file_format in ('yaml', 'yml'):
        return yaml.load(file_data, Loader=yaml.FullLoader)
    else:
        raise TypeError(
            'Please, choose a file with the appropriate format')
