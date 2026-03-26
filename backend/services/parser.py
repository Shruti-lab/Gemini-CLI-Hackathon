import pandas as pd
import json
import os

def parse_excel(file_path):
    """Reads an Excel file and converts it into a structured JSON format."""
    try:
        # Load the Excel file
        df = pd.read_excel(file_path)
        
        # Convert the DataFrame to a list of dictionaries (JSON-like structure)
        data = df.to_dict(orient='records')
        
        return data
    except Exception as e:
        print(f"Error parsing Excel file: {e}")
        return None
