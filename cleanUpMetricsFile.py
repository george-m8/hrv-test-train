import pandas as pd
import sys

def remove_duplicates(input_csv, output_csv):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(input_csv)
    
    # Drop duplicate rows
    df_cleaned = df.drop_duplicates()
    
    # Save the cleaned DataFrame to a new CSV file
    df_cleaned.to_csv(output_csv, index=False)
    print(f"Cleaned CSV saved to {output_csv}")

def main():
    if len(sys.argv) != 3:
        print("Usage: python remove_duplicates.py <input_csv> <output_csv>")
        sys.exit(1)

    input_csv = sys.argv[1]
    output_csv = sys.argv[2]

    try:
        remove_duplicates(input_csv, output_csv)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
