import os
import numpy as np

def file_exists(file_name, extension, *args):
    # Construct the directory path
    directory_path = os.path.join(".", *args)
    file_name = os.path.splitext(file_name)[0]
    file_name = f"{file_name}.{extension}"
    file_path = os.path.join(directory_path, file_name)
    
    if os.path.exists(file_path):
        print(f"File {file_path} already exists, skipping...")
        return True
    else:
        return False

def save_numpy_file(data, file_name, *args):
    """
    Save a numpy array to a specified directory structure.

    Parameters:
    - data: numpy array to be saved
    - file_name: name of the file (without extension)
    - *args: additional arguments representing directory structure
    """
    # Construct the directory path
    directory_path = os.path.join(".", *args)
    
    # Ensure the directory exists
    os.makedirs(directory_path, exist_ok=True)
    
    # Construct the full file path
    file_path = os.path.join(directory_path, f"{file_name}.npy")
    
    # Save the numpy array to the file
    np.save(file_path, data)
    
    print(f"File saved to {file_path}")

# Example usage
if __name__ == "__main__":
    # Example numpy data
    data = np.array([1, 2, 3, 4, 5])
    
    # Example function call
    save_numpy_file(data, "3420809148", "hfd", "kmax=5", "norm=true")
