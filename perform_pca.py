import sys
import os
import pandas as pd
from sklearn.preprocessing import StandardScaler 
from sklearn.decomposition import PCA

debug = True

# Function to list CSV files in a directory
def list_csv_files(directory):
    return [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.csv')]

def load_csv_data(file_path):
    # Load the compiled MFCC data from CSV
    data = pd.read_csv(file_path)
    if debug:
        print(f"Loaded .csv file: {file_path}")
    return data

def preprocess_data(data, exclude_columns):
    # Exclude non-MFCC columns (like userID and ground truth)
    data = data.drop(columns=exclude_columns)
    if debug:
        print("Excluded columns: ", exclude_columns)
    return data

def standardize_data(data):
    # Standardize the data (mean=0, variance=1)
    scaler = StandardScaler()
    standardized_data = scaler.fit_transform(data)
    if debug:
        print("Standardized data")

    return standardized_data

def apply_pca(data, n_components):
    # Apply PCA for dimensionality reduction
    pca = PCA(n_components=n_components)
    if debug:
        print(f"Applying PCA with {n_components} components")
    pca_result = pca.fit_transform(data)
    return pca_result, pca.explained_variance_ratio_

def main(data, n_components):
    # Load the data from CSV
    csv_file_path = data
    csv_data = load_csv_data(csv_file_path)

    # Store the csv file name
    csv_file_name = os.path.basename(csv_file_path)
    
    # Preprocess the data
    exclude_columns = ['HRV (ms)']  # Columns to exclude from PCA
    data = preprocess_data(csv_data, exclude_columns)
    
    # Standardize the data
    standardized_data = standardize_data(data)
    
    if debug:
        print("Shape of standardized data: ", standardized_data.shape)
        print("Max: ", standardized_data.max())
        print("Min: ", standardized_data.min())
    
    # Apply PCA
    pca_result, explained_variance = apply_pca(standardized_data, n_components)
    
    print(f"Explained variance by component: {explained_variance}")
    
    # Optionally save the PCA result to a new CSV
    pca_df = pd.DataFrame(pca_result)

    # Need to add back the 'HRV (ms)' column, append as first column
    pca_df.insert(0, 'HRV (ms)', csv_data['HRV (ms)'])

    # Create a new directory to store PCA features
    os.makedirs("pca_features", exist_ok=True)

    pca_df.to_csv(f"./pca_features/{csv_file_name}_pca_n_components={n_components}.csv", index=False)
    
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python perform_pca.py <csv directory>")
        sys.exit(1)
    else:
        # get file path from command line argument
        directory = sys.argv[1]
        files = list_csv_files(directory)

        print(f"Found {len(files)} CSV files in the directory.")

        n_components_array = [5, 10, 20, 50, 100]
        
        for file in files:
            for n_components in n_components_array:
                print(f"Processing file: {file}")
                print(f"Number of components: {n_components}")
                main(file, n_components)