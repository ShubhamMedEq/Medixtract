# PDF file No. R000530 - R000547 M. Gutierrez_Allied Health_Billing

import pdfplumber
import pandas as pd
import re
from datetime import datetime
from extractors.utils import extract_hospital_name


def extract_billing_info_pdf3(file_path):
    """Extract billing data from PDF 3."""
    data = []

    # Open PDF and extract text from each page
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                data.append({'page': page.page_number, 'text': text})

    # Extract hospital name from the first page
    hospital_name = extract_hospital_name(data[0]['text'])

    # Extract records from invoice details (first part of the PDF)
    df_invoice = extract_invoice_details(data[3]['text'], hospital_name)

    # Extract records from the health claim form (second part of the PDF)
    df_claim = allied_health_claim_form(data, start_page=4)

    # Combine the data into one DataFrame and return it
    return pd.concat([df_invoice, df_claim], ignore_index=True)


def extract_invoice_details(text, hospital_name):
    """Extract invoice details from the PDF."""
    # Define regex patterns
    date_pattern = r'\b(\d{1,2}/\d{1,2}/\d{4})\b'  # Matches dates in MM/DD/YYYY format
    description_pattern = r'([A-Za-z\s\.\-]+Appt\. No Show Fee)'  # Matches specific descriptions
    amount_pattern = r'\b(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\b'  # Matches monetary values

    # Extract values using regex
    dates = re.findall(date_pattern, text)
    descriptions = re.findall(description_pattern, text)
    amounts = re.findall(amount_pattern, text)

    # Extract the last amount as Balance Due (if available)
    balance_due = float(amounts[-1].replace(',', '')) if amounts else 0.0

    # Create records based on extracted values
    records = []
    for i, description in enumerate(descriptions):
        record = {
            "PROVIDER": hospital_name,  # Using the provided hospital_name here
            "DATE": datetime.strptime(dates[i], '%m/%d/%Y') if i < len(dates) else None,
            "CPT": None,  # No CPT code available for this section
            "DESCRIPTION": description.strip().upper(),
            "CHARGES": balance_due if i == len(descriptions) - 1 else float(amounts[i].replace(',', ''))
        }
        records.append(record)

    # Return the extracted data as a DataFrame
    return pd.DataFrame(records)


def allied_health_claim_form(data, start_page=4):
    """Extract claim form details from the PDF."""
    date_pattern = r'(\d{2} \d{2} \d{2})'
    service_line_pattern = r'(\d{2} \d{2} \d{2}).+?(\b[A-Z]?\d{4,5}\b).+?(\d+)' # Date + CPT code + Charges pattern

    hospital_name = extract_hospital_name(data[0]['text'])

    records = []

    for page_data in data[start_page:]:
        text = page_data['text']

        dates = re.findall(date_pattern, text)
        from_date = datetime.strptime(dates[0], '%m %d %y') if dates else None
        to_date = datetime.strptime(dates[-1], '%m %d %y') if len(dates) > 1 else None

        service_lines = re.findall(service_line_pattern, text)

        for service_date, code, charge in service_lines:
            service_date_obj = datetime.strptime(service_date, '%m %d %y')

            record = {
                "PROVIDER": hospital_name,
                "DATE": service_date_obj,
                "CPT": str(code),
                "DESCRIPTION": None,  # No description provided here
                "CHARGES": float(charge)
            }
            records.append(record)

    return pd.DataFrame(records)