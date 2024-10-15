import os
import sys
import numpy as np
import pandas as pd

from cachingScripts import cache_features
from compile_features import *
    
# define function to merge two dataframes based on 'ID' column
def merge_dataframes(dfA, dfB):
    return pd.merge(dfA, dfB, on='ID')

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python concatenate_compile_featurs.py <directoryA> <directoryB>')
        sys.exit(1)
    else:
        directoryA = sys.argv[1]
        directoryB = sys.argv[2]

        file_extensions = ['.npy', '.csv']
        directories_a = get_directories_with_files(directoryA, file_extensions)
        directories_b = get_directories_with_files(directoryB, file_extensions)

        for features_directory_a in directories_a:
            df_a = npy_to_dataframe(features_directory_a)
            nice_name_a = generate_nice_name(features_directory_a)
            print(f'Nice name A input: {features_directory_a}')
            print(f'Nice name A output: {nice_name_a}')
            for features_directory_b in directories_b:
                # Compile directories individually from npy files to df
                df_b = npy_to_dataframe(features_directory_b)
                # Get nice names for directories
                nice_name_b = generate_nice_name(features_directory_b)
                print(f'Nice name B input: {features_directory_b}')
                print(f'Nice name B output: {nice_name_b}')

                # Join the two dataframe based on the 'ID' column
                merged_df = merge_dataframes(df_a, df_b)

                # Merge with lookup.csv
                merged_df = merge_with_lookup(merged_df, 'lookup.csv')

                # Drop the 'ID' column
                merged_df = drop_id_column(merged_df)

                merged_df = drop_empty_hrv_rows(merged_df)

                # Save the merged dataframe to a csv file
                cache_features(f'./concatenated_features/{nice_name_a}+{nice_name_b}.csv', merged_df)
                print(f'Cached {nice_name_a} with {nice_name_b} at ./concatenated_features/{nice_name_a}+{nice_name_b}.csv')

'''
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
'''