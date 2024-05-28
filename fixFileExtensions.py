import os
import subprocess
import json
import sys

# Uses FFProbe to identify contained file type and renames the file with correct extension.

def get_format_details(file_path):
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        result_json = json.loads(result.stdout)
        format_name = result_json['format']['format_name']
        format_long_name = result_json['format'].get('format_long_name', 'N/A')
        codec_long_name = 'N/A'
        for stream in result_json.get('streams', []):
            if stream['codec_type'] == 'audio':
                codec_long_name = stream.get('codec_long_name', 'N/A')
                break
        return format_name, format_long_name, codec_long_name
    except Exception as e:
        return f"Error: {e}", "N/A", "N/A"

def get_extension_for_format(format_name, codec_long_name):
    # Lookup for specific formats
    if "webm" in format_name:
        return "webm"
    elif "mov" in format_name:
        return "mov"
    elif "ogg" in format_name:
        return "ogg"
    elif "wav" in format_name:
        return "wav"
    
    # Default None if format is not recognized
    return None

def rename_files_based_on_format(folder_path, log_file):
    deleted_files_count = 0
    with open(log_file, 'w') as log:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                format_name, format_long_name, codec_long_name = get_format_details(file_path)
                if "Error" not in format_name:
                    new_extension = get_extension_for_format(format_name, codec_long_name)
                    if new_extension:
                        new_file_name = f"{os.path.splitext(file)[0]}.{new_extension}"
                        new_file_path = os.path.join(root, new_file_name)
                        os.rename(file_path, new_file_path)
                        log.write(f"Renamed: {file} to {new_file_name} | Format: {format_name} ({format_long_name}), Codec: {codec_long_name}\n")
                    else:
                        os.remove(file_path)
                        deleted_files_count += 1
                        log.write(f"Deleted: {file} | Unrecognized format: {format_name} ({format_long_name}), Codec: {codec_long_name}\n")
                else:
                    os.remove(file_path)
                    deleted_files_count += 1
                    log.write(f"Deleted: {file} | Reason: {format_name}\n")
        print(f"Total files deleted: {deleted_files_count}")
        log.write(f"\nTotal files deleted: {deleted_files_count}\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fixFileExtensions.py <folder_path>")
        sys.exit(1) 
    folder_path = sys.argv[1]
    
    log_file = "./logs/fixFileExtensions.log"
    rename_files_based_on_format(folder_path, log_file)
    print(f"Renaming and logging process completed. Check {log_file} for details.")
