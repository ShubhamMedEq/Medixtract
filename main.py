from mypdfocr import process_pdf
from mapping import main as process_mapping

def main(input_pdf, output_pdf, json_output):
    """
    Main function to process the PDF and extract services.

    Parameters:
    input_pdf (str): Path to the input PDF file.
    output_pdf (str): Path to the output searchable PDF file.
    json_output (str): Path to save the extracted text in JSON format.
    """
    # Step 1: Process the PDF to extract text and save it as JSON
    process_pdf(input_pdf, output_pdf, json_output)

    # Step 2: Process the JSON to extract services and save to Excel
    process_mapping(json_output)

if __name__ == "__main__":
    input_pdf = "24.08.22 Janice Joubert - 1st choice_BILL.pdf"
    output_pdf = "output_ocr.pdf"
    json_output = "output.json"

    main(input_pdf, output_pdf, json_output)
