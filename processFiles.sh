#!/bin/bash

# Define the local directory
LOCAL_DIRECTORY="./hrv-audio-recs"

# Count files and print result
count=$(ls $LOCAL_DIRECTORY | wc -l)
echo "Number of files: $count"

# Run Python script to fix the audio file extensions
python fixFileExtensions.py $LOCAL_DIRECTORY

# Run Python script to standardise files to 16-bit, 16kHz, mono, PCM/wav format.
python convertToPCM.py $LOCAL_DIRECTORY

# Run Python script to delete duplicate audio files
python deleteDuplicates.py $LOCAL_DIRECTORY

# Run Python script to rename files. Files will have content after first "-" removed. Duplicate names will be iterated with a number in brackets if necessary.
python renameFiles.py $LOCAL_DIRECTORY

# Count files and print result
count=$(ls $LOCAL_DIRECTORY | wc -l)
echo "Number of files: $count"

# Run Python script to identify files with short duration and/or excessively low volume
python cleanUpAudioDir.py $LOCAL_DIRECTORY --min_duration 10 --volume_threshold -100

# Count files and print result
count=$(ls $LOCAL_DIRECTORY | wc -l)
echo "Number of files: $count"

# Run Python script to trim silence from start and end of audio files
python trimSilence.py $LOCAL_DIRECTORY

# Run "cleanUpAudioDir.py" again with more harsh parameters to delete files that are now too short or too quiet. Since the files feature no starting or ending silence, average volume should now be a more precise measure.
python cleanUpAudioDir.py $LOCAL_DIRECTORY --min_duration 6 --volume_threshold -40

# Count files and print result
count=$(ls $LOCAL_DIRECTORY | wc -l)
echo "Number of files: $count"