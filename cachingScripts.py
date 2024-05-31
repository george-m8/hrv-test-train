import os
import sys

from fileSaveScripts import save_dataframe_to_csv

def directory_exists(path: str) -> bool:
    """
    Check if a directory exists.

    Args:
        path (str): The directory path to check.

    Returns:
        bool: True if the directory exists, False otherwise.
    """
    return os.path.isdir(path)

def file_exists(path: str) -> bool:
    """
    Check if a file exists.

    Args:
        path (str): The file path to check.

    Returns:
        bool: True if the file exists, False otherwise.
    """
    return os.path.isfile(path)

# Function to combine file path, file name, and extension into a full path
def combine_path(file_path, file_name, extension):
    # Combine file path, file name, and extension
    full_path = os.path.join(file_path, f"{file_name}{extension}")   
    return full_path

def cache_features(file_path, df):
    overwrite_cache = True
    if not overwrite_cache:
        if file_exists(file_path):
            print(f"The file {file_path} exists.")
            return file_path
        else:
            return save_dataframe_to_csv(df, file_path)
    else:
        return save_dataframe_to_csv(df, file_path)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python cachingScripts.py <wav_file_path>")
        sys.exit(1)    
    else:

        path = sys.argv[1]
        if directory_exists(path):
            print(f"The directory {path} exists.")
        else:
            print(f"The directory {path} does not exist.")