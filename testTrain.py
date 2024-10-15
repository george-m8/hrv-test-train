import os
import sys
import csv
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_squared_error
import numpy as np

models = {
    'LinearRegression': {
        'model': LinearRegression(),
        'params': {}
    },
    'Ridge': {
        'model': Ridge(),
        'params': {'alpha': [0.1, 1.0, 10.0]}
    },
    'Lasso': {
        'model': Pipeline([
            ('scaler', StandardScaler()),
            ('lasso', Lasso())
        ]),
        'params': {
            'lasso__alpha': [0.1, 1.0, 10.0],
            'lasso__max_iter': [1000, 5000, 10000]
        }
    },
    'RandomForest': {
        'model': RandomForestRegressor(),
        'params': {'n_estimators': [10, 50, 100]}
    }
}
# Function to list CSV files in a directory
def list_csv_files(directory):
    return [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.csv')]

# Function to split data into train and test sets
def split_data(df, test_size=0.2, random_state=42):
    X = df.iloc[:, 1:]  # features
    y = df.iloc[:, 0]   # target
    return train_test_split(X, y, test_size=test_size, random_state=random_state)

def train_model(X_train, y_train, model, params):
    grid_search = GridSearchCV(estimator=model, param_grid=params, cv=5, scoring='neg_mean_squared_error')
    grid_search.fit(X_train, y_train)
    return grid_search.best_estimator_

def evaluate_model(model, X_test, y_test, model_name, feature_name):
    y_pred = model.predict(X_test)
    # Print y_test and y_pred to debug
    print(f"y_test:{y_test}")
    print(f"y_pred:{y_pred}")
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
        "correlation": correlation,
        "y_test": y_test,
        "y_pred": y_pred
    }

def append_results_to_csv(result, output_file):
    file_exists = os.path.isfile(output_file)

    with open(output_file, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["model_name", "model_params", "feature_name", "predictions_file", "r2_score", "mse", "correlation"])
        
        if not file_exists:
            writer.writeheader()
        
        writer.writerow({
            "model_name": result["model_name"],
            "model_params": result["model_params"],
            "feature_name": result["feature_name"],
            "predictions_file": result["predictions_file"],
            "r2_score": result["r2_score"],
            "mse": result["mse"],
            "correlation": result["correlation"]
        })

def generate_filename(model_name, params, feature_name, output_dir="predictions"):
    params_str = "_".join([f"{k}={v}" for k, v in params.items()])
    filename = f"{model_name}_{params_str}_{feature_name}.csv"
    return os.path.join(output_dir, filename)

def save_predictions_to_csv(y_test, y_pred, model_name, params, feature_name):
    # Create output directory if it doesn't exist
    output_dir = "predictions"
    os.makedirs(output_dir, exist_ok=True)
    
    filename = generate_filename(model_name, params, feature_name, output_dir)
    
    # Save the predictions to a CSV file
    predictions_df = pd.DataFrame({'y_test': y_test, 'y_pred': y_pred})
    predictions_df.to_csv(filename, index=False)
    print(f"Saved predictions to {filename}")
    return filename

# Define the list_csv_files function (mock implementation for example)
def list_csv_files(directory):
    return [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.csv')]

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

        for model_name, model_info in models.items():
            print(f"Training {model_name} model...")
            model = train_model(X_train, y_train, model_info['model'], model_info['params'])

            result = evaluate_model(model, X_test, y_test, model_name, feature_name)
            
            # Save actual vs predicted values
            predictions_file = save_predictions_to_csv(result["y_test"], result["y_pred"], model_name, model_info['params'], feature_name)

            # Append predictions file to result variable
            result["predictions_file"] = predictions_file

            print(result)

            append_results_to_csv(result, "model_evaluation_results.csv")

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
        #results_df = pd.DataFrame(results)
        #results_df.to_csv("model_evaluation_results.csv", index=False)