import os
import sys
import csv
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import numpy as np

# Function to list CSV files in a directory
def list_csv_files(directory):
    return [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.csv')]

# Function to split data into train and test sets
def split_data(df, test_size=0.2, random_state=42):
    X = df.iloc[:, 1:]  # features
    y = df.iloc[:, 0]   # target
    return train_test_split(X, y, test_size=test_size, random_state=random_state)

# Function to train a regression model
def train_model(X_train, y_train):
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test, model_name, feature_name):
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    correlation = np.corrcoef(y_test, y_pred)[0, 1]
    
    print(f"Model: {model_name}, Feature: {feature_name}")
    print(f"R2 Score: {r2}")
    print(f"Mean Squared Error: {mse}")
    print(f"Correlation: {correlation}")
    
    return {
        "model_name": model_name,
        "model_params": model.get_params(),
        "feature_name": feature_name,
        "r2_score": r2,
        "mse": mse,
        "correlation": correlation
    }

def append_results_to_csv(results, output_file):
    file_exists = os.path.isfile(output_file)

    with open(output_file, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["model_name", "model_params", "feature_name", "r2_score", "mse", "correlation"])
        
        if not file_exists:
            writer.writeheader()
        
        for result in results:
            writer.writerow({
                "model_name": result["model_name"],
                "model_params": result["model_params"],
                "feature_name": result["feature_name"],
                "r2_score": result["r2_score"],
                "mse": result["mse"],
                "correlation": result["correlation"]
            })

# Main function to iterate over files, train and evaluate models
def main(directory):
    results = []
    files = list_csv_files(directory)

    print(f"Found {len(files)} CSV files in the directory.")
    
    for file in files:
        df = pd.read_csv(file)
        print(f"Processing file: {file}")
        feature_name = os.path.basename(file).split('.')[0]
        print(f"Feature name: {feature_name}")
        
        X_train, X_test, y_train, y_test = split_data(df)
        
        model = train_model(X_train, y_train)
        
        result = evaluate_model(model, X_test, y_test, "LinearRegression", feature_name)
        results.append(result)

        append_results_to_csv(results, "model_evaluation_results.csv")
    
    return results

# Example usage
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python testTrain.py <csv_directory>")
        sys.exit(1)
    else:
        directory = sys.argv[1]
        results = main(directory)
        # Optionally, you can save results to a CSV file or further process them
        results_df = pd.DataFrame(results)
        results_df.to_csv("model_evaluation_results.csv", index=False)