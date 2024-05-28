#!/bin/bash

# Define the S3 bucket and local directory
BUCKET_NAME="hrv-audio-recs"
LOCAL_DIRECTORY="./hrv-audio-recs"

# Create the local directory if it doesn't exist
mkdir -p "$LOCAL_DIRECTORY"

# Count files and print result
count=$(ls $LOCAL_DIRECTORY | wc -l)
echo "Number of files: $count"

# Check directory for existing files. If present, ask user if they would like to delete and if so, delete.
python deleteFilesFromDirectory.py $LOCAL_DIRECTORY

# Sync the entire bucket with the local directory
aws s3 sync s3://$BUCKET_NAME $LOCAL_DIRECTORY

# Count files and print result
count=$(ls $LOCAL_DIRECTORY | wc -l)
echo "Number of files: $count"
