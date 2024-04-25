# Underlined dark-on-light green.
default_color_label = "4;32;40"

def colored_print(s: str, color_label=default_color_label, end='\n') -> None:
    print(f'\x1b[{color_label}m' + s + '\x1b[0m', end=end)
