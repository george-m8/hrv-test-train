import os
import numpy as np
import soundfile as sf

def higuchi_fd(signal, kmax=5, norm=True):
    # Optionally normalize the signal
    if norm:
        signal = (signal - np.mean(signal)) / np.std(signal)

    # Higuchi's Fractal Dimension calculation
    N = len(signal)
    Lmk = np.zeros((kmax, kmax))
    for k in range(1, kmax + 1):
        for m in range(1, k + 1):
            Lmki = 0
            for i in range(1, int(np.floor((N - m) / k))):
                Lmki += abs(signal[m + i * k] - signal[m + (i - 1) * k])
            norm_factor = (N - 1) / (k * int(np.floor((N - m) / k)) * k)
            Lmk[m - 1, k - 1] = norm_factor * Lmki
    Lk = np.sum(Lmk, axis=0) / kmax
    lnLk = np.log(Lk)
    lnk = np.log(1.0 / np.arange(1, kmax + 1))
    HFD = -np.polyfit(lnk, lnLk, 1)[0]
    return HFD

def extractHFD(file_path, kmax=5, norm=True):
    log_file="./logs/extractHFD.log"

    # Read the audio file
    signal, sample_rate = sf.read(file_path)

    # Extract HFD with provided parameters
    hfd_feature = higuchi_fd(signal, kmax, norm)

    # Log relevant details
    with open(log_file, 'a') as log:
        log.write(f"File: {os.path.basename(file_path)}\n")
        log.write(f"HFD Value: {hfd_feature}\n")
        log.write(f"Parameters: kmax={kmax}, norm={norm}\n\n")

    # Define output directory
    output_dir = os.path.join('speechFeatures', 'hfd_features')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Save feature as numpy array
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    np.save(os.path.join(output_dir, base_name), hfd_feature)

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python extract_hfd.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    extractHFD(file_path)
    print(f"Finished processing file: {file_path}")
