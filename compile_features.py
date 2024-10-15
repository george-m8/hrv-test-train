import os
import sys
import numpy as np
import pandas as pd

from fileSaveScripts import save_dataframe_to_csv
from cachingScripts import cache_features

def npy_to_dataframe(directory):
    data = []
    filenames = []

    # Iterate through all files in the directory
    for file in os.listdir(directory):
        if file.endswith(".npy"):
            file_path = os.path.join(directory, file)
            # Load the .npy file
            array_data = np.load(file_path)
            
            # Flatten and convert the data to a list
            if np.isscalar(array_data) or array_data.ndim == 0:
                array_data = [array_data.item()]
            else:
                array_data = array_data.flatten().tolist()
            
            # Add the filename (minus .npy) and data to the list
            filenames.append(os.path.splitext(file)[0])
            data.append(array_data)

    print(f"Data: {data[:10]}")
    # Determine the maximum length for padding
    max_length = max(len(row) for row in data)
    padded_data = [row + [0] * (max_length - len(row)) for row in data]

    # Convert to DataFrame and insert filenames
    df = pd.DataFrame(padded_data)
    df.insert(0, 'ID', filenames)
    
    #print(df[:10])
    
    return df

def merge_with_lookup(input, csv_file):
    # If directory is not a dataframe, convert it to a dataframe
    if not isinstance(input, pd.DataFrame):
        df_npy = npy_to_dataframe(directory)
    else:
        df_npy = input

    # Read the CSV file
    df_csv = pd.read_csv(csv_file)

    # Merge DataFrames on the filename and Prolific ID
    merged_df = pd.merge(df_npy, df_csv[['Prolific ID', 'HRV (ms)']], left_on='ID', right_on='Prolific ID')

    # Drop the duplicate column 'Prolific ID' and rename 'filename' to 'PID'
    merged_df = merged_df.drop(columns=['Prolific ID'])

    # Reorder columns to place 'HRV (ms)' as the second column
    cols = merged_df.columns.tolist()
    cols.insert(1, cols.pop(cols.index('HRV (ms)')))
    merged_df = merged_df[cols]

    return merged_df

def drop_id_column(df):
    return df.drop(columns=['ID'])

def drop_empty_hrv_rows(df):
    # Remove rows where 'HRV (ms)' is NaN
    df_cleaned = df.dropna(subset=['HRV (ms)'])
    return df_cleaned

def get_directories_with_files(base_path, file_extensions):
    directories_with_files = []

    for root, dirs, files in os.walk(base_path):
        # Check if the current directory contains any files with the specified extensions
        if any(file.endswith(tuple(file_extensions)) for file in files):
            directories_with_files.append(root)

    return directories_with_files

def generate_nice_name(path):
    top_level_dir = './speechFeatures'
    # Get the relative path and remove the top level directory prefix
    relative_path = os.path.relpath(path, f'./{top_level_dir}')
    if relative_path.startswith(os.path.basename(top_level_dir)):
        relative_path = relative_path[len(os.path.basename(top_level_dir)) + 1:]
    # Replace '/' with '_'
    nice_name = relative_path.replace(os.sep, '_')
    # Remove any leading '_'
    if nice_name.startswith('_'):
        nice_name = nice_name[1:]
    return nice_name

def compile_and_cache_features(path):
    file_extensions = ['.npy', '.csv']
    directories = get_directories_with_files(path, file_extensions)
    num_directories = len(directories)
    for directory in directories:
        nice_name = generate_nice_name(directory)
        print(f'Processing {nice_name}...')
        print(f'{directories.index(directory) + 1}/{num_directories}')
        #df = npy_to_dataframe(directory)
        df = merge_with_lookup(directory, 'lookup.csv')
        df = drop_id_column(df)
        df = drop_empty_hrv_rows(df)
        cache_features(f'./cached_features/{nice_name}.csv', df)
        print(f'Cached {nice_name} at ./cached_features/{nice_name}.csv')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python npy_to_dataframe.py <directory>')
        sys.exit(1)
    else:
        directory = sys.argv[1]
        compile_and_cache_features(directory)
        '''
        #df = npy_to_dataframe(directory)
        df = merge_with_lookup(directory, 'lookup.csv')
        save_dataframe_to_csv(df, '/test_csvs/merged_data.csv')
        df = drop_id_column(df)
        save_dataframe_to_csv(df, '/test_csvs/noID_merged_data.csv')
        df = drop_empty_hrv_rows(df)
        save_dataframe_to_csv(df, '/test_csvs/noEmptyHrv_merged_data.csv')
        #print(df)
        '''
        '''
        file_extensions = ['.npy', '.csv'] # List of file extensions to search for within directories
        base_directory = './speechFeatures'
    
        # Get the list of directories with files
        directories = get_directories_with_files(base_directory, file_extensions)
        # Generate and print nice names for each directory
        print("Directories with files:")
        for directory in directories:
            print(directory)
        
        print("\nNice names:")
        for directory in directories:
            nice_name = generate_nice_name(directory)
            print(nice_name)

        '''