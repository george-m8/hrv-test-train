import os
import csv
import pandas as pd
import numpy as np
from sklearn.metrics import r2_score, mean_squared_error


# Function to evaluate a model
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

    filename = generate_filename(model_name, params, feature_name, output_dir) # Creating issues since file name is greater than 255 chars. Suggest storing some file name data as a hash. Maybe these details could be stored as first two lines of the csv data?

    predictions_df = pd.DataFrame({'y_test': y_test, 'y_pred': y_pred})
    predictions_df.to_csv(filename, index=False)
    print(f"Saved predictions to {filename}")

# Function to evaluate, append results to CSV, and save predictions, all in one
def evaluate_and_save(model, X_test, y_test, model_name, feature_name, output_file, params, save_predicition):
    result = evaluate_model(model, X_test, y_test, model_name, feature_name)
    append_results_to_csv(result, output_file)
    if save_predicition:
        save_predictions_to_csv(y_test, result["y_pred"], model_name, params, feature_name)