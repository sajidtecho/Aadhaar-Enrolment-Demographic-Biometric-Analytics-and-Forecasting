import pandas as pd
import os

file_path = r"c:\Users\Shakil Ahmad\OneDrive\Desktop\UIDAI\Adhar_biometric\01_data\raw\Aadhar Seva Kendra List.xlsx"

try:
    df = pd.read_excel(file_path)
    # Print columns to see what we have
    print("Columns:", df.columns.tolist())
    
    # Try to filter for Delhi. Adjust column names based on print output if needed.
    # Assuming there's a State or City column.
    
    # Let's inspect the first few rows to guess structure if column names aren't obvious
    print(df.head())
    
except Exception as e:
    print(f"Error: {e}")
