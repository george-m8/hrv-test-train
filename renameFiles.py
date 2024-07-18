import os
import re
import sys

# Removes hyphens from files and appends iterated numbers within brackets to the end of the file if the name already exists.

def clean_filename(filename):
    """Removes everything to the right of and including the first hyphen, keeping the file extension if present."""
    name, extension = os.path.splitext(filename)
    cleaned_name = name.split('-', 1)[0]
    return cleaned_name + extension

def remove_bracketed_number(filename):
    """Removes the bracketed number from the filename."""
    return re.sub(r'\(\d+\)', '', filename).strip()

def get_new_filename(directory, base_name, extension):
    """Finds the next available filename by incrementing the number in brackets."""
    counter = 1
    new_name = f"{base_name}{extension}"
    while os.path.exists(os.path.join(directory, new_name)):
        new_name = f"{base_name}({counter}){extension}"
        counter += 1
    return new_name

def rename_files(directory, log_file):
    with open(log_file, 'a') as log:
        for filename in os.listdir(directory):
            original_path = os.path.join(directory, filename)
            if os.path.isfile(original_path):
                new_name = filename

                if '-' in filename:
                    new_name = clean_filename(filename)
                elif re.search(r'\(\d+\)\.[a-zA-Z0-9]+$', filename):
                    # Check if the file has a bracketed number and attempt to rename it
                    candidate_name = remove_bracketed_number(filename)
                    candidate_path = os.path.join(directory, candidate_name)

                    if not os.path.exists(candidate_path):
                        new_name = candidate_name
                    elif candidate_path != original_path:
                        # Find the next available name
                        base_name, extension = os.path.splitext(candidate_name)
                        new_name = get_new_filename(directory, base_name, extension)

                if new_name != filename:
                    final_path = os.path.join(directory, new_name)
                    os.rename(original_path, final_path)
                    log.write(f"Renamed '{filename}' to '{new_name}'\n")
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
