import os
import argparse
from pydub import AudioSegment
from pydub.utils import mediainfo

def is_low_volume(audio, threshold):
    """Check if the audio has very low volume."""
    return audio.dBFS < threshold

def log_message(log_file, message):
    """Log a message to the log file."""
    with open(log_file, 'a') as log:
        log.write(f"{message}\n")

def main(directory, min_duration, volume_threshold, log_file):
    deleted_files = []
    problematic_files = []

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            audio = AudioSegment.from_file(file_path)
            duration_seconds = len(audio) / 1000.0

            if duration_seconds < min_duration or is_low_volume(audio, volume_threshold):
                os.remove(file_path)
                deleted_files.append(file_path)
                log_message(log_file, f"Deleted {file_path}: duration={duration_seconds:.2f}s, volume={audio.dBFS:.2f}dBFS")
            else:
                log_message(log_file, f"Keeping {file_path}: duration={duration_seconds:.2f}s, volume={audio.dBFS:.2f}dBFS")

        except Exception as e:
            log_message(log_file, f"Error processing {file_path}: {str(e)}")
            problematic_files.append(file_path)
    
    print(f"\nDeleted {len(deleted_files)} files.")
    log_message(log_file, f"\nDeleted {len(deleted_files)} files.")
    if problematic_files:
        log_message(log_file, f"{len(problematic_files)} files encountered problems during processing and were not deleted:")
        for file in problematic_files:
            log_message(log_file, file)
        
        print(f"{len(problematic_files)} files encountered problems during processing and were not deleted:")
        for file in problematic_files:
            print(file)

        delete_problematic = input("Do you want to delete the problematic files? (y/n): ").strip().lower()
        if delete_problematic == 'y':
            for file in problematic_files:
                try:
                    os.remove(file)
                    log_message(log_file, f"Deleted problematic file {file}")
                except Exception as e:
                    log_message(log_file, f"Error deleting problematic file {file}: {str(e)}")
            print("Problematic files have been deleted.")
        else:
            print("Problematic files were not deleted.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Delete audio files shorter than a given duration or with low volume.")
    parser.add_argument("directory", type=str, help="The directory containing the audio files.")
    parser.add_argument("--min_duration", type=float, default=10.0, help="Minimum duration in seconds to keep an audio file.")
    parser.add_argument("--volume_threshold", type=float, default=-50.0, help="Minimum volume in dBFS to keep an audio file.")

    logFile= "./logs/cleanUpAudioDir.log"    
    args = parser.parse_args()
    main(args.directory, args.min_duration, args.volume_threshold, logFile)
