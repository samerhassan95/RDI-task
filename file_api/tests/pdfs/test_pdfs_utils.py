import pytest
from file_api.utils.pdfs_utils import extract_pdf_metadata
from io import BytesIO
from PyPDF2 import PdfWriter, PageObject


# Utility function to create a valid PDF in memory
def create_valid_pdf():
    pdf_writer = PdfWriter()
    
    # Create a blank page
    page = PageObject.create_blank_page(width=612, height=792)
    
    # Add the page to the writer
    pdf_writer.add_page(page)
    
    pdf_data = BytesIO()
    pdf_writer.write(pdf_data)
    pdf_data.seek(0)
    
    return pdf_data


@pytest.mark.django_db
def test_extract_pdf_metadata_valid():
    # Create a valid PDF
    pdf_data = create_valid_pdf()
    
    # Save the PDF to a temporary location
    with open("test.pdf", "wb") as f:
        f.write(pdf_data.read())
    
    # Test metadata extraction
    metadata = extract_pdf_metadata("test.pdf")
    
    assert metadata['page_count'] == 1
    assert 'page_width' in metadata
    assert 'page_height' in metadata
    
    # Clean up
    import os
    os.remove("test.pdf")


@pytest.mark.django_db
def test_extract_pdf_metadata_invalid():
    # Test with a non-PDF file or invalid PDF content
    invalid_pdf_data = BytesIO(b"Invalid PDF content")
    
    # Save the invalid PDF to a temporary location
    with open("invalid_test.pdf", "wb") as f:
        f.write(invalid_pdf_data.read())
    
    # Test that extracting metadata from an invalid PDF raises an error
    with pytest.raises(ValueError, match="Error extracting PDF metadata"):
        extract_pdf_metadata("invalid_test.pdf")
    
    # Clean up
    import os
    os.remove("invalid_test.pdf")
