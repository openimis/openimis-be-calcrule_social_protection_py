import ast


def convert_to_python_value(string):
    try:
        value = ast.literal_eval(string)
        return value
    except (SyntaxError, ValueError):
        return string
