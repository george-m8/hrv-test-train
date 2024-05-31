import os
import sys
import numpy as np

from featureExtractScripts import higuchi_fd, calculate_dfa2, get_f0_values, calculate_jitter_shimmer
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

                extract_hfd = True
                extract_dfa2 = True
                extract_f0 = True
                extract_jitter_shimmer = False # Broken
                
                if extract_hfd:
                    feature_name = "higuchi_fd"
                    kmax_values = [2, 3, 5, 7, 10]
                    norm_values = [True, False]
                    for kmax in kmax_values:
                        for norm in norm_values:
                            if not file_exists(file_name, saved_file_extension, "speechFeatures", feature_name, f"kmax={kmax}", f"norm={norm}"):
                                extractedFeature = higuchi_fd(file_path, kmax, norm)
                                save_file(extractedFeature, file_name, "speechFeatures", feature_name, f"kmax={kmax}", f"norm={norm}")

                if extract_dfa2:
                    feature_name = "dfa2"
                    overlap_values = [True, False]
                    order_values = [1, 2]

                    for overlap in overlap_values:
                        for order in order_values:
                            if not file_exists(file_name, saved_file_extension, "speechFeatures", feature_name, f"overlap={overlap}", f"order={order}"):
                                extractedFeature = calculate_dfa2(file_path, overlap=overlap, order=order)
                                save_file(extractedFeature, file_name, "speechFeatures", feature_name, f"overlap={overlap}", f"order={order}")
                    
                if extract_f0:
                    feature_name = "f0"
                    if not file_exists(file_name, saved_file_extension, "speechFeatures", feature_name, "default"):
                        extractedFeature = np.concatenate(get_f0_values(file_path))
                        save_file(extractedFeature, file_name, "speechFeatures", feature_name, "all_f0_values", "default")

                if extract_jitter_shimmer:
                    feature_name = "jitter_shimmer"
                    if not file_exists(file_name, saved_file_extension, "speechFeatures", feature_name, "default"):
                        extractedFeature = calculate_jitter_shimmer(file_path)
                        save_file(extractedFeature, file_name, "speechFeatures", feature_name, "default")
                

        log.write(f"Feature extraction script completed.\n\n")

if __name__ == "__main__":

    log_file = "./logs/extractFeatures.log"

    if len(sys.argv) != 2:
        print("Usage: python extractFeatures.py <directory>")
    else:
        directory = sys.argv[1]
        main(directory,log_file)