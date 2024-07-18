import os
import sys
import numpy as np

from featureExtractScripts import higuchi_fd, calculate_dfa2, get_f0_values
from fileSaveScripts import save_numpy_file, file_exists, save_temp_file

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
                    nvals=[256, 512, 1024, 2048, 4096, 8192, 16384, 32768]
                    overlap_values = [True, False]
                    order_values = [1]
                    fit_trend_values = ['poly']
                    fit_exp_values = ['RANSAC']
                    debug_plot_value = False

                    for overlap in overlap_values:
                        for order in order_values:
                            for fit_trend in fit_trend_values:
                                for fit_exp in fit_exp_values:
                                    if not file_exists(file_name, saved_file_extension, "speechFeatures", feature_name, f"overlap={overlap}", f"order={order}", f"nvals={nvals}", f"fit_trend={fit_trend}", f"fit_exp={fit_exp}"):
                                        extractedFeature, temp_file = calculate_dfa2(file_path, overlap=overlap, order=order, fit_trend=fit_trend, fit_exp=fit_exp, nvals=nvals, debug_plot=debug_plot_value)
                                        save_file(extractedFeature, file_name, "speechFeatures", feature_name, f"overlap={overlap}", f"order={order}", f"nvals={nvals}", f"fit_trend={fit_trend}", f"fit_exp={fit_exp}")
                                        if temp_file is not None:
                                            save_temp_file(temp_file, file_name, "debug", feature_name, f"overlap={overlap}", f"order={order}", f"nvals={nvals}", f"fit_trend={fit_trend}", f"fit_exp={fit_exp}")
                        
                if extract_f0:
                    feature_name = "f0"
                    if not file_exists(file_name, saved_file_extension, "speechFeatures", feature_name, "default"):
                        extractedFeature = np.concatenate(get_f0_values(file_path))
                        save_file(extractedFeature, file_name, "speechFeatures", feature_name, "all_f0_values", "default")
                

        log.write(f"Feature extraction script completed.\n\n")

if __name__ == "__main__":

    log_file = "./logs/extractFeatures.log"

    if len(sys.argv) != 2:
        print("Usage: python extractFeatures.py <directory>")
    else:
        directory = sys.argv[1]
        main(directory,log_file)