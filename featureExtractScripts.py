import numpy as np
import librosa
import nolds
import parselmouth
from parselmouth.praat import call

def higuchi_fd(file_path, kmax, norm):
    """
    Compute the Higuchi Fractal Dimension (HFD) of a signal.

    Parameters:
    file_path (str): Path to the input audio file.
    kmax (int): Maximum k value for the HFD calculation.
    norm (bool): If True, normalize the signal.

    Returns:
    float: Higuchi Fractal Dimension of the signal, or None if an error occurs.
    """
    try:
        # Load the audio file
        signal, _ = librosa.load(file_path, sr=None)

        # Ensure the audio is mono
        if signal.ndim > 1:
            signal = librosa.to_mono(signal)

        # Optionally normalize the signal
        if norm:
            signal = (signal - np.mean(signal)) / np.std(signal)

        N = len(signal)
        if kmax >= N:
            print(f"Error: kmax ({kmax}) must be smaller than the length of the signal ({N}).")
            return None

        Lmk = np.zeros((kmax, kmax))
        for k in range(1, kmax + 1):
            for m in range(1, k + 1):
                Lmki = 0
                for i in range(1, int(np.floor((N - m) / k))):
                    Lmki += abs(signal[m + i * k] - signal[m + (i - 1) * k])
                norm_factor = (N - 1) / (k * int(np.floor((N - m) / k)) * k)
                Lmk[m - 1, k - 1] = norm_factor * Lmki

        Lk = np.sum(Lmk, axis=0) / kmax

        # Remove zero or negative values before taking the log
        Lk = Lk[Lk > 0]
        if len(Lk) == 0:
            print("Error: All Lk values are non-positive, cannot compute logarithm.")
            return None

        lnLk = np.log(Lk)
        lnk = np.log(1.0 / np.arange(1, len(Lk) + 1))

        if len(lnk) < 2:
            print("Error: Not enough valid points for polyfit.")
            return None

        try:
            HFD = -np.polyfit(lnk, lnLk, 1)[0]
        except np.linalg.LinAlgError as e:
            print(f"Polyfit error: {e}")
            return None

        return HFD

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def calculate_dfa2(audio_file_path, **kwargs):
    """
    Calculate the DFA2 value of an audio file.
    
    Parameters:
    - audio_file_path: str, path to the audio file
    - nvals: list of int, window sizes for DFA (default is calculated internally by nolds)
    - overlap: bool, whether to use overlapping windows (default is True)
    - order: int, order of polynomial for detrending (default is 1)
    - fit_trend: str, method to fit the trend ('poly' or other options in nolds)
    - fit_exp: str, method to fit the exponent ('RANSAC' or other options in nolds)
    - debug_plot: bool, whether to plot debug information (default is False)
    - debug_data: bool, whether to return debug data (default is False)
    - plot_file: str, file to save debug plot (default is None)
    
    Returns:
    - DFA2 value if successful, None if there is an error
    """
    # Default parameters
    params = {
        "nvals": None,
        "overlap": True,
        "order": 1,
        "fit_trend": 'poly',
        "fit_exp": 'RANSAC',
        "debug_plot": False,
        "debug_data": False,
        "plot_file": None
    }
    
    # Update default parameters with any provided keyword arguments
    params.update(kwargs)
    
    try:
        # Load audio file
        y, sr = librosa.load(audio_file_path)
        
        # Ensure the audio is mono
        if y.ndim > 1:
            y = np.mean(y, axis=1)
        
        # Calculate DFA2 using nolds
        dfa2_value = nolds.dfa(
            y,
            nvals=params['nvals'],
            overlap=params['overlap'],
            order=params['order'],
            fit_trend=params['fit_trend'],
            fit_exp=params['fit_exp'],
            debug_plot=params['debug_plot'],
            debug_data=params['debug_data'],
            plot_file=params['plot_file']
        )
        
        print(f"DFA2 value: {dfa2_value}")
        return dfa2_value
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


import librosa
import numpy as np

def calculate_jitter_shimmer(file_path, **kwargs):
    try:
        # Load the WAV file with parselmouth (which uses Praat)
        snd = parselmouth.Sound(file_path)
        
        # Apply pre-emphasis if specified
        preemphasis = kwargs.get('preemphasis', None)
        if preemphasis is not None:
            snd = snd.copy()
            snd.pre_emphasis(filter_frequency=preemphasis)
        
        # Calculate jitter
        point_process = call(snd, "To PointProcess (periodic, cc)", 75, 500)
        jitter_local = call(point_process, "Get jitter (local)", 0, 0.02, 1.3, 1.6)
        
        # Calculate shimmer
        shimmer_local = call([snd, point_process], "Get shimmer (local)", 0, 0.02, 1.3, 1.6, 1.3)
        
        # Create an array with jitter and shimmer values
        result_array = np.array([jitter_local, shimmer_local])
        
        return result_array
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None