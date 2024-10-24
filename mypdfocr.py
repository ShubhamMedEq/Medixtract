import json
import ocrmypdf
import pdfplumber


def process_pdf(input_pdf_path, output_pdf_path, json_output_path):
    """
    Process a PDF file to create a searchable PDF using OCR, 
    then extract the text and save it as a JSON file.

    Parameters:
    input_pdf_path (str): Path to the input PDF file.
    output_pdf_path (str): Path to the output searchable PDF file.
    json_output_path (str): Path to save the extracted text in JSON format.
    """
    # Step 1: Use OCRmyPDF to create a searchable PDF
    ocrmypdf.ocr(input_pdf_path, output_pdf_path, force_ocr=True)

    # Step 2: Extract text from the OCR-processed PDF
    extracted_text = []

    with pdfplumber.open(output_pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                extracted_text.append({
                    'page': page.page_number,
                    'text': text
                })

    # Step 3: Save extracted text as JSON
    with open(json_output_path, 'w') as json_file:
        json.dump(extracted_text, json_file, indent=4)

    print("OCR processing and text extraction complete.")


# Example usage
if __name__ == "__main__":
    input_pdf = '24.08.22 Janice Joubert - 1st choice_BILL.pdf'
    output_pdf = 'output_ocr.pdf'
    json_output = 'output.json'

    process_pdf(input_pdf, output_pdf, json_output)
