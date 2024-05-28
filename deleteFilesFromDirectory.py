import os
import sys
import shutil

# Deletes all files in a directory if the directory is not empty. TO BE USED BEFORE RUNNING THE S3 SYNC TO AVOID DUPLICATES.

def check_and_delete_files(directory):
    if os.path.exists(directory) and os.listdir(directory):
        choice = input(f"The folder {directory} contains files. Do you want to delete all files in this folder before proceeding? (y/n): ").strip().lower()
        if choice == 'y':
            print(f"Deleting all files in {directory}...")
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f'Failed to delete {file_path}. Reason: {e}')
        elif choice == 'n':
            print("Proceeding without deleting files...")
        else:
            print("Invalid choice. Exiting script.")
            sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <directory>")
        sys.exit(1)
    else:
        directory = sys.argv[1]
        check_and_delete_files(directory)
