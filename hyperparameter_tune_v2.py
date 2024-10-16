import os
import datetime
import sys
import csv
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.metrics import r2_score, mean_squared_error
import numpy as np
import optuna

from save_prediction_evaluation import evaluate_and_save

# Function to list CSV files in a directory
def list_csv_files(directory):
    return [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.csv')]

# Define models and their corresponding hyperparameters
def get_model_params():
    return {
        "LinearRegression": {
            "model": LinearRegression(),
            "params": {}
        },
        "Ridge": {
            "model": Ridge(),
            "params": {
                "alpha": lambda trial: trial.suggest_float("alpha", 1e-3, 10.0)
            }
        },
        "Lasso": {
            "model": Lasso(),
            "params": {
                "alpha": lambda trial: trial.suggest_float("alpha", 1e-3, 10.0)
            }
        },
        "RandomForestRegressor": {
            "model": RandomForestRegressor(),
            "params": {
                "n_estimators": lambda trial: trial.suggest_int('n_estimators', 10, 200),
                "max_depth": lambda trial: trial.suggest_int('max_depth', 2, 32),
                "min_samples_split": lambda trial: trial.suggest_int('min_samples_split', 2, 20),
                "min_samples_leaf": lambda trial: trial.suggest_int('min_samples_leaf', 1, 20)
            }
        }
    }

# Function to split data into train and test sets, now with feature engineering
def split_data(df, test_size=0.2, random_state=42):
    X = df.iloc[:, 1:]  # features
    y = df.iloc[:, 0]   # target
    
    # Apply feature engineering (Polynomial and Interaction features)
    poly = PolynomialFeatures(degree=2, include_bias=False)
    X_poly = poly.fit_transform(X)
    
    scaler = StandardScaler()
    X_poly_scaled = scaler.fit_transform(X_poly)
    
    return train_test_split(X_poly_scaled, y, test_size=test_size, random_state=random_state)

# General objective function for hyperparameter tuning with Optuna
def objective(trial, model_class, X_train, y_train):
    params = model_class["params"]
    model = model_class["model"]
    
    # Set model parameters based on the trial
    model_params = {param_name: param_fn(trial) for param_name, param_fn in params.items()}
    model.set_params(**model_params)
    
    # Fit the model
    model.fit(X_train, y_train)
    y_pred = model.predict(X_train)
    mse = mean_squared_error(y_train, y_pred)
    
    return mse

# Hyperparameter tuning function
def hyperparameter_tuning(model_class, X_train, y_train):
    if not model_class["params"]:
        return model_class["model"].get_params()  # No tuning for models without hyperparameters

    # Create Optuna study
    study = optuna.create_study(direction='minimize')
    study.optimize(lambda trial: objective(trial, model_class, X_train, y_train), n_trials=100)
    
    return study.best_params

# Function to evaluate the model
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

# Append results to CSV
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

# Generate filename for predictions
def generate_filename(model_name, params, feature_name, output_dir="predictions"):
    params_str = "_".join([f"{k}={v}" for k, v in params.items()])
    filename = f"{model_name}_{params_str}_{feature_name}.csv"
    return os.path.join(output_dir, filename)

# Save predictions to CSV
def save_predictions_to_csv(y_test, y_pred, model_name, params, feature_name):
    output_dir = "predictions"
    os.makedirs(output_dir, exist_ok=True)

    filename = generate_filename(model_name, params, feature_name, output_dir)

    # If file name is longer than 250 characters, truncate it but keep extension
    if len(filename) > 250:
        filename = filename[:250] + filename[-4:]

    predictions_df = pd.DataFrame({'y_test': y_test, 'y_pred': y_pred})
    predictions_df.to_csv(filename, index=False)
    print(f"Saved predictions to {filename}")

# Evaluate all models
def evaluate_all_models(X_train, X_test, y_train, y_test, feature_name):
    results = []
    model_classes = get_model_params()

    for model_name, model_class in model_classes.items():
        print(f"Processing model: {model_name}")
        
        # Perform hyperparameter tuning if applicable
        best_params = hyperparameter_tuning(model_class, X_train, y_train)
        print(f"Best params for {model_name}: {best_params}")
        
        # Train the model
        model = model_class["model"]
        model.set_params(**best_params)
        model.fit(X_train, y_train)

        # Evaluate the model
        result = evaluate_model(model, X_test, y_test, model_name, feature_name)
        results.append(result)

        # Use datetime to store current date (not time) as variable
        date = datetime.datetime.now().date()

        # Save results and predictions
        append_results_to_csv(result, f"{date}_model_evaluation_results.csv")
        save_predictions_to_csv(result["y_test"], result["y_pred"], model_name, model.get_params(), feature_name)

    return results

# Main function to iterate over files, train and evaluate models
def main(path):
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

        X_train, X_test, y_train, y_test = split_data(df)

        # Evaluate all models
        results = evaluate_all_models(X_train, X_test, y_train, y_test, feature_name)
        print(results)

    return results

# Example usage
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python testTrain.py <csv_directory>")
        sys.exit(1)
    else:
        directory = sys.argv[1]
        results = main(directory)
