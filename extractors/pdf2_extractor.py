# PDF file No. R000548 - R000550 M. Gutierrez_EMG Center Of Houston_Billing

import fitz  # PyMuPDF
import re
from datetime import datetime
import pandas as pd
from extractors.utils import extract_hospital_name

def extract_billing_info_pdf2(file_path):
    """Extract billing data from PDF 2."""
    doc = fitz.open(file_path)
    billing_records = []

    # Extract hospital name from the first page
    hospital_name = extract_hospital_name(doc[0].get_text(sort=True))

    # Loop through PDF pages
    for page in doc:
        text = page.get_text(sort=True)

        # Regex to extract date, CPT, description, units, and charges
        pattern = r'(\d{4})\s+(\d{2}/\d{2}/\d{4})\s+(.+?)\s+([A-Z0-9]+)\s+([\d,]+\.\d{2})' # date, CPT, description, units, and charges
        matches = re.findall(pattern, text)

        for match in matches:
            record = {
                "PROVIDER": hospital_name,
                "DATE": datetime.strptime(match[1], '%m/%d/%Y'),
                "CPT": str(match[3]),
                "DESCRIPTION": match[2].strip().upper(),
                "CHARGES": float(match[4].replace(',', ''))
            }
            billing_records.append(record)

    return pd.DataFrame(billing_records)