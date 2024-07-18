import os
import sys
import csv
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_squared_error
import numpy as np
import optuna

# Function to list CSV files in a directory
def list_csv_files(directory):
    return [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.csv')]

# Function to split data into train and test sets
def split_data(df, test_size=0.2, random_state=42):
    X = df.iloc[:, 1:]  # features
    y = df.iloc[:, 0]   # target
    return train_test_split(X, y, test_size=test_size, random_state=random_state)

def objective(trial, X_train, y_train):
    n_estimators = trial.suggest_int('n_estimators', 10, 200)
    max_depth = trial.suggest_int('max_depth', 2, 32)
    min_samples_split = trial.suggest_int('min_samples_split', 2, 20)
    min_samples_leaf = trial.suggest_int('min_samples_leaf', 1, 20)

    model = RandomForestRegressor(
        n_estimators=n_estimators,
        max_depth=max_depth,
        min_samples_split=min_samples_split,
        min_samples_leaf=min_samples_leaf
    )

    model.fit(X_train, y_train)
    y_pred = model.predict(X_train)
    mse = mean_squared_error(y_train, y_pred)
    return mse

def hyperparameter_tuning(X_train, y_train):
    study = optuna.create_study(direction='minimize')
    study.optimize(lambda trial: objective(trial, X_train, y_train), n_trials=100)
    return study.best_params

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
        "correlation": correlation,
        "y_test": y_test,
        "y_pred": y_pred
    }

def append_results_to_csv(result, output_file):
    file_exists = os.path.isfile(output_file)

    with open(output_file, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["model_name", "model_params", "feature_name", "r2_score", "mse", "correlation"])

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            "model_name": result["model_name"],
            "model_params": result["model_params"],
            "feature_name": result["feature_name"],
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

# Main function to iterate over files, train and evaluate models
def main(path):
    results = []
    
    if os.path.isfile(path):
        files = [path]
        print(f"Processing single file: {path}")
    else:
        files = list_csv_files(path)
        print(f"Found {len(files)} CSV files in the directory.")

    for file in files:
        df = pd.read_csv(file)
        print(f"Processing file: {file}")
        feature_name = os.path.basename(file).split('.')[0]
        print(f"Feature name: {feature_name}")

        X_train, X_test, y_train, y_test = split_data(df)

        # Hyperparameter tuning using Optuna
        best_params = hyperparameter_tuning(X_train, y_train)
        print(f"Best params for RandomForest: {best_params}")

        # Train the best model
        best_rf_model = RandomForestRegressor(**best_params)
        best_rf_model.fit(X_train, y_train)

        result = evaluate_model(best_rf_model, X_test, y_test, 'RandomForest', feature_name)
        print(result)

        append_results_to_csv(result, "model_evaluation_results.csv")

        # Save actual vs predicted values
        save_predictions_to_csv(result["y_test"], result["y_pred"], 'RandomForest', best_params, feature_name)

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
        # results_df = pd.DataFrame(results)
        # results_df.to_csv("model_evaluation_results.csv", index=False)
