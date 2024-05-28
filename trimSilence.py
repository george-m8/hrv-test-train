import os
import sys
from pydub import AudioSegment
from pydub.silence import detect_nonsilent

def trim_silence(audio, silence_thresh=-50, chunk_size=10):
    """Trim silence from the beginning and end of an audio segment."""
    non_silence = detect_nonsilent(audio, min_silence_len=chunk_size, silence_thresh=silence_thresh)
    if non_silence:
        start_trim = non_silence[0][0]
        end_trim = non_silence[-1][1]
        return audio[start_trim:end_trim], start_trim, len(audio) - end_trim
    return audio, 0, 0

def process_audio_files(input_folder, log_file, silence_thresh=-50, chunk_size=10):
    """Process all audio files in the input folder and overwrite them with trimmed versions."""
    with open(log_file, 'a') as log:
        for filename in os.listdir(input_folder):
            audio_path = os.path.join(input_folder, filename)
            audio = AudioSegment.from_file(audio_path)
            trimmed_audio, start_trim, end_trim = trim_silence(audio, silence_thresh, chunk_size)
            
            # Log the details
            log.write(f"{filename}\n")
            log.write(f"Total Length: {len(audio)} ms\n")
            log.write(f"Trim at Start: {start_trim} ms\n")
            log.write(f"Trim at End: {end_trim} ms\n\n")
            
            # Overwrite the original file with the trimmed audio
            file_format = filename.split('.')[-1]
            trimmed_audio.export(audio_path, format=file_format)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_folder>")
        sys.exit(1)
    
    input_folder = sys.argv[1]
    log_file = "./logs/trimSilence.log"

    # Process audio files
    process_audio_files(input_folder, log_file)
