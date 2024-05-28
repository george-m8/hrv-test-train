A series of scripts for using audio recordings to train a machine learning model. With the end goal of predicting HRV (heart rate variance) from an input audio file.

My previous project, "voiceRecorder-standalone" is being used to collect audio data via a web browser. This forwards a user to a Google sheet where they provide data about their current HRV as well as other details. This data is sent to an AWS S3 bucket where this project can access it.

Currently, this project syncs from AWS S3 and takes a number of steps to process the data:
- Download all files from S3
- Fix file extensions for files uploaded with incorrect or missing extensions using FFProbe to analyse contained audio type.
- Rename files, removing time data from the file names, making files easier to work with later.
- Delete duplicates by comparing MD5 hash.
- Delete quiet and short duration audio files.

I am currently working on further clean up scripts:
- Convert all files to WAV/PCM with standardised channels, sample rate, and format/extension.
    - This should replace all files in the folder. It's currently duplicating them. Further work here required.
    - This should be inserted to syncS3.sh after fixing file extensions.
- Trim silence from start and end.
    - Should be ready to go.
    - Should be inserted to syncS3.sh before "cleanUpAudioDir.py" instruction.

## To do
- [x] Finalise convertToPCM.py script
- [x] Finalise and run trim trimSilence.py script
- [ ] Delete audio files that do not appear on lookup.csv
- [ ] Delete lines from lookup.csv that do not appear as audio files.
- [ ] Noise reduce audio
- [ ] Identify numerical data types to extract from audio files (speech features)
    - [ ] Create modular script for this:
       - [x] Iterate through folder
       - [x] Extract metric
       - [x] Save to appropriate folder as .npy array file.
       - [ ] I think there's further scope to modularise this, for example: Can we just write a script that will process the audio and send back signal and sample rate. If this is used multiple times this will be more slick.
   - [ ] Potential extractions:
       - [ ] DFA2
       - [x] HFD
       - [ ] Other fractals
       - [ ] MFCC with varying parameters
- [ ] Create script to compile ground truth data with speech features
   - [ ] Compile data from .npy or .csv speech feature files
   - [ ] Save compiled data to a cache as a .csv
   - [ ] Provide the user an option to ignore, force overwrite, use/not use cache.
- [ ] Split data for test and train
- [ ] Test and train with various regression machines
   - [ ] Output result metrics to an evaluation .csv file.
- [ ] Introduce hyper parameter tuning to identify the best settings for machines.