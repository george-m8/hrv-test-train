#!/bin/bash

# Define the S3 bucket and local directory
BUCKET_NAME="hrv-audio-recs"
LOCAL_DIRECTORY="./hrv-audio-recs"
BUCKET_REGION="us-west-2"

# Create the local directory if it doesn't exist
mkdir -p "$LOCAL_DIRECTORY"

# Count files and print result
count=$(ls $LOCAL_DIRECTORY | wc -l)
echo "Number of files: $count"

# Check directory for existing files. If present, ask user if they would like to delete and if so, delete.
python deleteFilesFromDirectory.py $LOCAL_DIRECTORY

# Sync the entire bucket with the local directory
aws s3 sync s3://$BUCKET_NAME $LOCAL_DIRECTORY --region $BUCKET_REGION

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