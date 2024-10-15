import sys
import pandas as pd
from sklearn.preprocessing import StandardScaler 
from sklearn.decomposition import PCA

debug = True

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
    data = load_csv_data(csv_file_path)
    
    # Preprocess the data
    exclude_columns = ['HRV (ms)']  # Columns to exclude from PCA
    data = preprocess_data(data, exclude_columns)
    
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
    pca_df.to_csv("pca_transformed_data.csv", index=False)
    
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python perform_pca.py <data.csv>")
        sys.exit(1)
    else:
        # get file path from command line argument
        file = sys.argv[1]
        main(file, 10)  # Perform PCA with 10 components