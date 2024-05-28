import os
import sys
import hashlib
from pydub import AudioSegment
from tqdm import tqdm

# Identifies duplicates and deletes a copy.

def write_log(log_file, message):
    with open(log_file, 'a') as f:
        f.write(f"{message}\n")

def calculate_hash(file_path):
    """Calculate the hash of an audio file."""
    audio = AudioSegment.from_file(file_path)
    raw_data = audio.raw_data
    return hashlib.md5(raw_data).hexdigest()

def find_duplicates(directory, log_file):
    write_log(log_file, f"Scanning directory: {directory}")

    if not os.path.isdir(directory):
        write_log(log_file, f"Directory does not exist: {directory}")
        return

    hash_dict = {}
    duplicates = []

    # Scan through the directory
    for root, _, files in os.walk(directory):
        for file in tqdm(files):
            file_path = os.path.join(root, file)
            try:
                file_hash = calculate_hash(file_path)
                if file_hash in hash_dict:
                    duplicates.append(file_path)
                    write_log(log_file, f"Duplicate found: {file_path} (Duplicate of {hash_dict[file_hash]})")
                else:
                    hash_dict[file_hash] = file_path
            except Exception as e:
                write_log(log_file, f"Error processing file {file_path}: {e}")

    # Delete duplicates
    for file_path in duplicates:
        try:
            os.remove(file_path)
            write_log(log_file, f"Deleted duplicate file: {file_path}")
        except Exception as e:
            write_log(log_file, f"Error deleting file {file_path}: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <directory>")
        sys.exit(1)

    directory = sys.argv[1]
    log_file = "./logs/deleteDuplicates.log"

    find_duplicates(directory, log_file)
