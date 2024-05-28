import os
import sys

from featureExtractScripts import extractHFD

def main(directory,log_file):
    with open(log_file, 'a') as log:
        if not os.path.exists(directory):
            print(f"The folder {directory} does not exist.")
            log.write(f"The folder {directory} does not exist./n")
            sys.exit(1)

        for file_name in os.listdir(directory):
            if file_name.endswith('.wav'):
                log.write(f"Processing {file_name}/n")
                file_path = os.path.join(directory, file_name)
                extractHFD(file_path)
        log.write(f"Feature extraction script completed./n/n")

if __name__ == "__main__":

    log_file = "./logs/extractFeatures.log"

    if len(sys.argv) != 2:
        print("Usage: python extractFeatures.py <directory>")
    else:
        directory = sys.argv[1]
        main(directory,log_file)