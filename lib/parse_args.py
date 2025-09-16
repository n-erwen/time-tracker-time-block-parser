import sys


def get_arg_flags(arg):
    return ['--' + arg['name']] + (['-' + arg['shorthand']] if arg['shorthand'] else [])


def parse_args(args):
    """Input format: {'name': str, 'shorthand': str, 'is_bool': bool}[]"""
    arg_index = 1  # start at first arg
    arg_values = {name: None for name in [arg['name'] for arg in args]}
    positional_values = []
    while arg_index < len(sys.argv):
        arg_set = False
        for arg in args:
            arg_flags = get_arg_flags(arg)
            if sys.argv[arg_index] in arg_flags and not arg_values[arg['name']]:
                if arg['is_bool']:
                    arg_values[arg['name']] = True
                    arg_set = True
                else:
                    arg_index += 1
                    arg_values[arg['name']] = sys.argv[arg_index]
                    arg_index += 1
                    arg_set = True
        if not arg_set:
            positional_values.append(sys.argv[arg_index])
            arg_index += 1
    return arg_values, positional_values
