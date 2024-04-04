import os
import pdf2image
import io
from PIL import Image
import pytesseract
from PyPDF2 import PdfWriter, PdfReader

pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR\tesseract.exe'  # Replace with your Tesseract path

def process_pdf(pdf_path, output_dir):
    """Converts a PDF file to searchable image-based PDF.

    Args:
        pdf_path (str): Path to the input PDF file.
        output_dir (str): Directory for storing the converted PDF.

    Returns:
        bool: True if conversion was successful, False otherwise.
    """

    try:
        pages = pdf2image.convert_from_path(pdf_path, 500, poppler_path='poppler-24.02.0/Library/bin')  # Adjust poppler path if needed

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        output_path = os.path.join(output_dir, os.path.basename(pdf_path))
        pdf_writer = PdfWriter()

        for page_num, page in enumerate(pages):
            im = page.copy()
            image = im.convert("RGB")

            page = pytesseract.image_to_pdf_or_hocr(image, extension='pdf', lang='eng')
            pdf = PdfReader(io.BytesIO(page))
            pdf_writer.add_page(pdf.pages[0])

        with open(output_path, "wb") as f:
            pdf_writer.write(f)

        print(f"Done processing: {os.path.basename(pdf_path)} ✔️")
        return True  # Indicate success

    except Exception as e:
        error_log_path = "error_log.txt"
        with open(error_log_path, "a") as log_file:
            log_file.write(f"File: {pdf_path}\n")
            log_file.write(f"Exception: {str(e)}\n\n")
        print(f"Error processing: {os.path.basename(pdf_path)} ❌")
        return False  # Indicate failure

# ... (Other functions as needed, but without multiprocessing) ...
