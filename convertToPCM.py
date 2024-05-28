from pydub import AudioSegment
import os
import sys

# Define the desired parameters
TARGET_SAMPLE_RATE = 16000
TARGET_CHANNELS = 1  # Mono
TARGET_FORMAT = "wav"
TARGET_EXTENSION = ".wav"
LOG_FILE = "./logs/convertToPCM.log"

# Ensure the script is called with the correct number of arguments
if len(sys.argv) != 2:
    print("Usage: python convert_audio.py <directory_path>")
    sys.exit(1)

input_folder = sys.argv[1]

# Open the log file for writing
with open(LOG_FILE, "w") as log_file:
    def log(message):
        log_file.write(message + "\n")
        print(message)
    
    def convert_audio(file_path):
        try:
            audio = AudioSegment.from_file(file_path)
            
            # Set the desired sample rate and number of channels
            audio = audio.set_frame_rate(TARGET_SAMPLE_RATE)
            audio = audio.set_channels(TARGET_CHANNELS)
            
            # Export the audio to the same file path, replacing the original
            audio.export(file_path, format=TARGET_FORMAT)
            log(f"Converted and replaced {file_path}")
        except Exception as e:
            log(f"Error converting {file_path}: {e}")

    # Iterate over all files in the directory
    for root, _, files in os.walk(input_folder):
        for file in files:
            file_path = os.path.join(root, file)
            convert_audio(file_path)

    log("Conversion process completed.")