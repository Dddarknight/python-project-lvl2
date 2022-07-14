# Gendiff
Gendiff is a Python library that shows the difference between two files in 3 optional formats.

____

### Hexlet tests and linter status:
[![Actions Status](https://github.com/Dddarknight/python-project-lvl2/workflows/hexlet-check/badge.svg)](https://github.com/Dddarknight/python-project-lvl2/actions)

[![Python CI](https://github.com/Dddarknight/python-project-lvl2/actions/workflows/pyci.yml/badge.svg)](https://github.com/Dddarknight/python-project-lvl2/actions)

### CodeClimate:
<a href="https://codeclimate.com/github/Dddarknight/python-project-lvl2/maintainability"><img src="https://api.codeclimate.com/v1/badges/f28009ac853edfa39fe8/maintainability" /></a>

<a href="https://codeclimate.com/github/Dddarknight/python-project-lvl2/test_coverage"><img src="https://api.codeclimate.com/v1/badges/f28009ac853edfa39fe8/test_coverage" /></a>

## Links
This project was built using these tools:
| Tool | Description |
|----------|---------|
| [poetry](https://python-poetry.org/) |  "Python dependency management and packaging made easy" |
| [Py.Test](https://pytest.org) | "A mature full-featured Python testing tool" |

## Description
Gendiff is a CLI utility.
The difference is shown in 3 formats:
| Format | Description |
|----------|---------|
| stylish (default) | Shows difference in the string format.  Shows elements that were added in the second file with "+", elements that were removed from the first file - with "-". All the elements in nested structures are included. |
| plain | Shows changes for the each element in the string format (only in the case of changing the element), with presenting the path of such element in the nested structure. |
| json | Returns a json-string with difference. Shows elements that were added in the second file with "+", elements that were removed from the first file - with "-".|

## Installation
```
$ git clone git@github.com:Dddarknight/python-project-lvl2.git
$ cd python-project-lvl2
$ python3 -m pip install dist/hexlet_code-0.1.0-py3-none-any.whl
```

## Usage
```
$ gendiff `file_path1` `file_path2`
$ gendiff `file_path1` `file_path2` --format plain
$ gendiff `file_path1` `file_path2` -f json

```

### Asciinema record:
[![asciinema](https://asciinema.org/a/htP3S68jeBmb0p8yWY6KHmfms.svg)](https://asciinema.org/a/htP3S68jeBmb0p8yWY6KHmfms)

## License
[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)
