import os
import sys
import numpy as np
import librosa
import traceback

from fileSaveScripts import save_numpy_file, file_exists

def save_file(data, file_name, *args):
    with open(log_file, 'a') as log:
        file_name = file_name.replace('.wav', '')
        if data is not None:
            save_numpy_file(data, file_name, *args)
            log.write(f"File saved as {file_name}\n")
        else:
            print(f"Error extracting feature from {file_name}")
            log.write(f"Error extracting feature from {file_name}\n")

def normalize_stft(stft):
    stft_normalized = librosa.util.normalize(stft)
    return stft_normalized

def extract_stft(file_path, window_length, hop_scale, normalise, log_file):
    try:
        y, sr = librosa.load(file_path)
        hop_length = int(window_length * hop_scale)
        stft = np.abs(librosa.stft(y, n_fft=window_length, hop_length=hop_length))
        if normalise:
            stft = normalize_stft(stft)
        with open(log_file, 'a') as log:
            log.write(f"STFT extracted successfully for file {file_path}\n")
        return stft
    except Exception as e:
        error_message = f"Error extracting STFT for file {file_path}: {e}\n{traceback.format_exc()}\n"
        print(error_message)
        with open(log_file, 'a') as log:
            log.write(error_message)
        return None
    
def flatten_numpy_array(array):
    return array.flatten()

def extract_features_from_segments(stft_data, window_length, hop_scale, normalize, log_file):
    features = []
    hop_length = int(window_length * hop_scale)

    num_frames = stft_data.shape[1]
    num_segments = (num_frames - window_length) // hop_length + 1
    
    with open(log_file, 'a') as log:
        for i in range(num_segments):
            segment = stft_data[:, i * hop_length : i * hop_length + window_length]
            if normalize:
                segment = normalize_stft(segment)
            segment_flattened = flatten_numpy_array(segment)
            features.append(segment_flattened)
        
        # Handle remaining part if the total length is not a multiple of window_length
        remaining_frames = num_frames % window_length
        if remaining_frames != 0:
            segment = stft_data[:, -remaining_frames:]
            # Pad with zeros to make it of window_length size
            padding_needed = window_length - remaining_frames
            segment = np.pad(segment, ((0, 0), (0, padding_needed)), 'constant')
            if normalize:
                segment = normalize_stft(segment)
            segment_flattened = flatten_numpy_array(segment)
            features.append(segment_flattened)
        
        feature_shape = np.array(features).shape
        log.write(f"Extracted STFT from segments for file STFT data.\n")
        log.write(f"Extracted feature with shape: {feature_shape}\n")
        return np.array(features)


def main(directory,log_file):
    with open(log_file, 'a') as log:
        if not os.path.exists(directory):
            print(f"The folder {directory} does not exist.")
            log.write(f"The folder {directory} does not exist.\n")
            sys.exit(1)

        saved_file_extension = "npy"

        for file_name in os.listdir(directory):
            if file_name.endswith('.wav'):
                log.write(f"Processing {file_name}\n")
                file_path = os.path.join(directory, file_name)

                extract_stft_bool = True
                extract_stft_segmented_bool = True
                
                if extract_stft_bool:
                    feature_name = "stft"
                    window_values = [320, 512, 1024]
                    hop_scale_values = [0.5, 0.25]
                    norm_values = [True, False]
                    for window in window_values:
                        for hop_scale in hop_scale_values:
                            hop_length = int(window * hop_scale)
                            for norm in norm_values:
                                if not file_exists(file_name, saved_file_extension, "speechFeatures", feature_name, f"window={window}", f"hop_length={hop_length}", f"norm={norm}"):
                                    extractedstft = extract_stft(file_path, window, hop_scale, norm, log_file)
                                    extractedstft_flattened = flatten_numpy_array(extractedstft)
                                    save_file(extractedstft_flattened, file_name, "speechFeatures", feature_name, f"window={window}", f"hop_length={hop_length}", f"norm={norm}")
                                    if(extract_stft_segmented_bool):
                                        extractedstft_segmented = extract_features_from_segments(extractedstft, window, hop_scale, norm, log_file)
                                        extractedstft_segmented_flattened = flatten_numpy_array(extractedstft_segmented)
                                        save_file(extractedstft_segmented_flattened, file_name, "speechFeatures", f"{feature_name}_segmented", f"window={window}", f"hop_length={hop_length}", f"norm={norm}")

        log.write(f"Feature extraction script completed.\n\n")

if __name__ == "__main__":

    log_file = "./logs/extractSTFT.log"

    if len(sys.argv) != 2:
        print("Usage: python extractFeatures.py <directory>")
    else:
        directory = sys.argv[1]
        main(directory,log_file)