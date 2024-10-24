# PDF file No. R000345 - R000349 M. Gutierrez_The Houston Spine & Rehabilitation Centers_Billing

import fitz  # PyMuPDF
import re
from datetime import datetime
import pandas as pd
from extractors.utils import extract_hospital_name

def extract_billing_info_pdf1(file_path):
    """Extract billing data from PDF 1."""
    doc = fitz.open(file_path)
    billing_records = []

    # Extract hospital name from the first page
    hospital_name = extract_hospital_name(doc[0].get_text(sort=True))

    # Loop through PDF pages
    for page in doc:
        text = page.get_text(sort=True)

        # Regex to extract date, CPT, description, units, and charges
        pattern = r'(\d{2}/\d{2}/\d{4})\s+Charge\s+[A-Za-z,\s]+\s+([A-Z0-9]*[0-9]+[A-Z0-9]*)\s+([\w\s\+\-\.\,\(\)]+)\s+(\d+\.\d{2})\s+(\d+\.\d{2})'
        matches = re.findall(pattern, text)

        for match in matches:
            record = {
                "PROVIDER": hospital_name,
                "DATE": datetime.strptime(match[0], '%m/%d/%Y'),
                "CPT": str(match[1]),
                "DESCRIPTION": match[2].strip().upper(),
                "CHARGES": float(match[4].replace(',', ''))
            }
            billing_records.append(record)

    return pd.DataFrame(billing_records)