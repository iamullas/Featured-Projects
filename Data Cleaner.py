import pandas as pd

def clean_csv(input_csv, output_csv):
    df = pd.read_csv(input_csv)
    # Remove duplicates and empty rows
    df = df.drop_duplicates().dropna()
    # Standardize text (e.g., lowercase names)
    df['name'] = df['name'].str.strip().str.title()
    df.to_csv(output_csv, index=False)
    print(f"Cleaned data saved to {output_csv}!")

# Example usage:
clean_csv('dirty_data.csv', 'clean_data.csv')