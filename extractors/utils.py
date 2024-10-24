# utils.py
import re
import pandas as pd

def extract_hospital_name(text):
    """Extract hospital name using regex."""
    match = re.search(r"FROM\s*:\s*([^\n]+)", text)
    return match.group(1).strip() if match else "Unknown Hospital"

def read_excel(file_path, sheet_name='CPT DESC'):
    """Read CPT Excel data into a DataFrame."""
    return pd.read_excel(file_path, sheet_name=sheet_name, dtype={'Procedure Code': str, 'Description': str})