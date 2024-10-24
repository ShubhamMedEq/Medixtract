import pandas as pd
import json
import re

# Function to extract services from text
def extract_services(text):
    """
    Extract services from a given text using a regex pattern.
    
    Parameters:
    text (str): The text containing service details.

    Returns:
    list: A list of extracted services.
    """
    # Refined regex pattern to match service details and avoid capturing extra data
    # Ensures that the description is followed by the CPT code (5 digits)
    pattern = r'(\d{2}/\d{2}/\d{4})\s+([^\d]+?)\s+(\d{5}(?:-\d{2})?)\s+(\d+)\s+\$(\d+\.\d{2})\s+\$(\d+\.\d{2})'

    # Replace multiple newlines with a space to avoid breaking entries in the middle
    text = text.replace('\n', ' ').replace('\r', ' ')

    # Find all matches in the text
    matches = re.findall(pattern, text)

    # Collecting services
    cleaned_services = []
    for match in matches:
        date, description, cpt_code, units, amount_per_unit, total_amount = match
        cleaned_services.append((date, description.strip(), cpt_code, units,
                                  f"${amount_per_unit}", f"${total_amount}"))

    return cleaned_services

# Load JSON data
def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Process each page and extract service information
def process_pages(json_data):
    all_services = []

    for page in json_data:
        text = page.get('text', '')

        # Extract services
        services = extract_services(text)

        # If no services were extracted and this might be the first entry, check manually
        if len(services) == 0:
            first_service_pattern = r'(\d{2}/\d{2}/\d{4})\s+([^\d]+?)\s+(\d{5}(?:-\d{2})?)\s+(\d+)\s+\$(\d+\.\d{2})\s+\$(\d+\.\d{2})'
            first_service_match = re.search(first_service_pattern, text)

            if first_service_match:
                date, description, cpt_code, units, amount_per_unit, total_amount = first_service_match.groups()
                services.append((date, description.strip(), cpt_code, units,
                                 f"${amount_per_unit}", f"${total_amount}"))

        all_services.extend(services)

    return all_services

# Main function to execute the script
def main(file_path):
    json_data = load_json(file_path)
    services = process_pages(json_data)

    # Create DataFrame
    columns = ["Date", "CPT Description", "CPT Code", "Units", "Amount Per Unit", "Total Amount"]
    services_df = pd.DataFrame(services, columns=columns)

    # Display the DataFrame
    print(services_df)

    # Optional: Save to Excel
    services_df.to_excel("services_provided.xlsx", index=False)

# Replace 'your_file.json' with the path to your JSON file
if __name__ == "__main__":
    main('/content/output.json')
