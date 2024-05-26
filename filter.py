import re

filter_table = {
    "single_quotes": r"'",
    "semicolon": r";",
    "comment_1": r"--",
    "comment_2": r"/\*.*\*/",
    "union": r"UNION",
    "or": r"OR",
    "and": r"AND",
    "delete": r"DELETE",
    "drop": r"DROP",
    "percent": r"%"
}

def filter_input(input_str: str):
    for key, pattern in filter_table.items():
        if re.search(pattern, input_str, re.IGNORECASE):
            raise ValueError(f"Invalid input: {key} detected in input.")
    return input_str
