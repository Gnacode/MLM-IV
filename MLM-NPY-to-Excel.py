import os
import numpy as np
import pandas as pd

# Directory containing the .npy files
data_directory = 'LMSIMDATA'  # Replace with your data directory path

# Set the current working directory to the script's execution directory
execution_directory = os.path.abspath(os.getcwd())  # Get the current working directory
data_directory = os.path.join(execution_directory, data_directory)  # Ensure full path
output_directory = os.path.join(data_directory, 'output')

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Iterate over all .npy files in the directory
for filename in os.listdir(data_directory):
    # Full file path
    file_path = os.path.join(data_directory, filename)

    # Check if it's a file and ends with .npy
    if os.path.isfile(file_path) and filename.endswith('.npy'):
        # Input file path
        input_file_path = os.path.join(data_directory, filename)
        
        # Output file path
        base_name = os.path.splitext(filename)[0]  # Remove .npy extension
        output_file_path = os.path.join(output_directory, f"{base_name}.xlsx")
        
        # Skip if output file already exists
        if os.path.exists(output_file_path):
            print(f"File already exists, skipping: {output_file_path}")
            continue
        
        # Load the .npy file
        try:
            data = np.load(input_file_path)
        except Exception as e:
            print(f"Error loading file {filename}: {e}")
            continue
        
        # Ensure data has the correct format (2D array with 2 rows)
        if data.shape[0] != 2:
            print(f"Invalid data format in file {filename}, skipping...")
            continue
        
        # Extract voltage and current
        voltage = data[0, :]  # First row
        current = data[1, :]  # Second row
        
        # Create a DataFrame
        df = pd.DataFrame({'Voltage (V)': voltage, 'Current (A)': current})
        
        # Save to an Excel file
        try:
            df.to_excel(output_file_path, index=False)
            print(f"Converted and saved: {output_file_path}")
        except Exception as e:
            print(f"Error saving file {output_file_path}: {e}")

print("Conversion complete.")
