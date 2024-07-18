A series of scripts for using audio recordings to train a machine learning model. With the end goal of predicting HRV (heart rate variance) from an input audio file.

My previous project, "voiceRecorder-standalone" is being used to collect audio data via a web browser. This forwards a user to a Google sheet where they provide data about their current HRV as well as other details. This data is sent to an AWS S3 bucket where this project can access it.

## To do
- [x] Finalise convertToPCM.py script
- [x] Finalise and run trim trimSilence.py script
- [x] Delete audio files that do not appear on lookup.csv
- [x] Delete lines from lookup.csv that do not appear as audio files.
- [ ] Noise reduce audio
- [x] Identify numerical data types to extract from audio files (speech features)
    - [x] Create modular script for this:
       - [x] Iterate through folder
       - [x] Extract metric
       - [x] Save to appropriate folder as .npy array file.

   - [ ] Potential extractions:
       - [x] DFA2
       - [x] HFD
       - [ ] Other fractals
       - [ ] MFCC with varying parameters
- [ ] Further Extractions
    - [ ] F0 median (in progress)
        - Can we do more with the arrays from F0?
        - Function currently either not working, or taking ages
    - [ ] Jitter and shimmer (in progress)
        - Error in function needs to be fixed.
    - [ ] Spectral Features
        - Method: Extract features like spectral centroid, spectral bandwidth, spectral contrast, and spectral flatness using Fourier transform.
    - [ ] Non-linear Dynamics
        - Method: Extract features such as correlation dimension, Lyapunov exponents, and entropy measures which capture the complexity of the signal.
        - Tools: TISEAN (a software package for nonlinear time series analysis).
    - [ ] Prosodic Features
        - Method: Analyze speech rate, rhythm, and intonation patterns.
        - Tools: OpenSMILE, Praat.
    - [ ] Glottal Flow Features
        - Method: Extract glottal flow parameters using inverse filtering techniques.
        - Tools: GLOTTAL-Flow, Praat.
    - [ ] Entropy Measures
        - Method: Compute measures like spectral entropy and Shannon entropy to quantify the randomness in the signal
- [x] Create script to compile ground truth data with speech features
   - [ ] Compile data from .npy or .csv speech feature files
   - [x] Save compiled data to a cache as a .csv
   - [ ] Provide the user an option to ignore, force overwrite, use/not use cache.
- [x] Split data for test and train
- [ ] Test and train with various regression machines
   - [x] Output result metrics to an evaluation .csv file.
- [ ] Introduce hyper parameter tuning to identify the best settings for machines.

## Potential Issues:
- [ ] What if I'd like to use an approach which leads to multiple files being created for each record? Currently we treat these as new records
- [ ] There are duplicates that appear, these could be in both test and train.
