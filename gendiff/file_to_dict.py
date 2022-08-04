import json
import yaml


def convert(file_data, file_format):
    if file_format == 'json':
        file_data_converted = json.load(file_data)
    elif file_format in ('yaml', 'yml'):
        file_data_converted = yaml.load(file_data, Loader=yaml.FullLoader)
    else:
        print('Please, choose a file with the appropriate format\
              (json, yml, yaml)')
        raise TypeError
    return file_data_converted
