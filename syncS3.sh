#!/bin/bash

# Define the S3 bucket and local directory
BUCKET_NAME="hrv-audio-recs"
LOCAL_DIRECTORY="./hrv-audio-recs"

# Create the local directory if it doesn't exist
mkdir -p "$LOCAL_DIRECTORY"

# Sync the entire bucket with the local directory
aws s3 sync s3://$BUCKET_NAME $LOCAL_DIRECTORY

# Run Python script to fix the audio file extensions
python fixFileExtensions.py $LOCAL_DIRECTORY

# Run Python script to rename files. Files will have content after first "-" removed. Duplicate names will be iterated with a number in brackets if necessary.
python renameFiles.py $LOCAL_DIRECTORY

# Run Python script to delete duplicate audio files
python deleteDuplicates.py $LOCAL_DIRECTORY

# Run Python script to identify files with short duration and/or excessively low volume
python cleanUpAudioDir.py $LOCAL_DIRECTORY --min_duration 10 --volume_threshold -50