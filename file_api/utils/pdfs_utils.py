from PyPDF2 import PdfReader

def extract_pdf_metadata(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        page_count = len(reader.pages)
        first_page = reader.pages[0]
        width = first_page.mediabox.width
        height = first_page.mediabox.height
        return {
            'page_count': page_count,
            'page_width': width,
            'page_height': height
        }
    except Exception as e:
        raise ValueError(f"Error extracting PDF metadata: {e}")
