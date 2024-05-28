import os
import re
import sys

def clean_filename(filename):
    # Use regex to isolate content before the first dash, if present
    match = re.match(r'^([a-zA-Z0-9]+)(?:-.*)?(\.[a-zA-Z0-9]+)$', filename)
    if match:
        return match.group(1) + match.group(2)
    else:
        return filename

def get_new_filename(directory, base_name, extension):
    new_name = f"{base_name}{extension}"
    counter = 1
    while os.path.exists(os.path.join(directory, new_name)):
        new_name = f"{base_name}({counter}){extension}"
        counter += 1
    return new_name

def remove_bracketed_number(filename):
    # Use regex to remove bracketed number at the end of filename
    return re.sub(r'\(\d+\)(\.[a-zA-Z0-9]+)$', r'\1', filename)

def rename_files(directory, log_file):
    with open(log_file, 'a') as log:
        for filename in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, filename)):
                new_name = filename

                if '-' in filename:
                    new_name = clean_filename(filename)
                elif re.search(r'\(\d+\)\.[a-zA-Z0-9]+$', filename):
                    # Check if the file has a bracketed number and attempt to rename it
                    candidate_name = remove_bracketed_number(filename)
                    if not os.path.exists(os.path.join(directory, candidate_name)):
                        new_name = candidate_name

                if new_name != filename:
                    base_name, extension = os.path.splitext(new_name)
                    final_name = get_new_filename(directory, base_name, extension)
                    os.rename(os.path.join(directory, filename), os.path.join(directory, final_name))
                    log.write(f"Renamed '{filename}' to '{final_name}'\n")
                else:
                    log.write(f"Left '{filename}' unchanged\n")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <directory_path>")
        sys.exit(1)
    
    directory_path = sys.argv[1]
    log_file = "./logs/renameFiles.log"

    
    if not os.path.isdir(directory_path):
        print(f"The directory {directory_path} does not exist.")
        sys.exit(1)
    
    rename_files(directory_path, log_file)
