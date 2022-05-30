import itertools


def normalize(x):
    if x is True:
        return 'true'
    elif x is False:
        return 'false'
    elif x is None:
        return 'null'
    else:
        return x


def stringify(value, depth, replacer='    '):

    def iter_(current_value, depth):
        if not isinstance(current_value, dict):
            return str(normalize(current_value))

        current_indent = replacer * (depth + 1)
        lines = []
        for key, val in current_value.items():
            lines.append(f'{current_indent}{key}: {iter_(val, depth+1)}')
        result = itertools.chain("{", lines, [current_indent[:-4] + "}"])
        return '\n'.join(result)

    return iter_(value, depth)
