#!/bin/bash

# Define features directory paths
FEATURES_DIRECTORY="./speechFeatures"
CACHED_FEATURES_DIRECTORY="./cached_features"

# Bool for whether to hyperparameter tune
HYPERPARAMETER_TUNING=true

# Start virtual environment
source venv/bin/activate

# Compile and cache the features
python compile_features.py $FEATURES_DIRECTORY

# If HYPERPARAMETER_TUNING is true, run hyperparameter_tuning, otherwise run testTrain
if [ "$HYPERPARAMETER_TUNING" = true ]; then
    # Hyperparameter tuning
    python hyperparameter_tuning.py $CACHED_FEATURES_DIRECTORY
else
    # Train the model
    python testTrain.py $CACHED_FEATURES_DIRECTORY
fi