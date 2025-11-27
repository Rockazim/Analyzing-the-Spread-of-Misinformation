import os
import matplotlib.colors as mcolors


def has_file_extension(file_path: str, file_extension: str) -> bool:
    """
    Checks if the file ends with the specified file extension.

    Args:
        file_path: The pathway to the file from the current directory.
        file_extension: The extension that a file is expected to end with.
    """
    has_file_extension = file_path.endswith(file_extension)
    if has_file_extension:
        return True
    else:
        print(f'Error: Only {file_extension} files are accepted. You attempted to insert "{file_path}".')
        return False
    

def file_exists(file_path: str, print_error_msg: bool=True) -> bool:
    """
    Checks if the file actually exists in the current directory.

    Args:
        file_path: The pathway to the file from the current directory.
        print_error_msg: Flag to indicate if error message should be printed out,
    """
    file_found = os.path.isfile(file_path)
    if file_found:
        return True
    else:
        if print_error_msg:
            print(f'Error: The file "{file_path}" does not exist.')
        return False


def file_empty(file_path: str) -> bool:
    """
    Checks if the file actually holds any data.

    Args:
        file_path: The pathway to the file from the current directory.
    """
    if os.path.getsize(file_path) == 0:
        print(f'Error: The inputted file "{file_path}" is empty.')
        return True
    else:
        return False
    

def get_csv_files(directory: str) -> list:
    """
    Returns list of all .csv files in the given directory.

    directory: The folder from which .csv files will be collected from.
    """
    csv_files = [
        os.path.join(directory, filename)
        for filename in os.listdir(directory)
        if filename.endswith(".csv")
        ]
    return csv_files


def validate_color(inputted_color: str) -> str:
    """
    Returns a valid color for the nodes to be plotted.

    Arg:
        inputted_color: The user-provided color to be verified.
    """
    if mcolors.is_color_like(inputted_color):
        return f"tab:{inputted_color}"
    else:
        print(f'Warning: The color "{inputted_color}" provided is not supported. Using default color for nodes.')
        return "tab:blue"


def remove_trailing_digits(s: str) -> str:
    """
    Returns string without numbers at the end.

    Args:
        s: The string to be manipulated.
    """
    while s and s[-1].isdigit():
        s = s[:-1]

    return s
