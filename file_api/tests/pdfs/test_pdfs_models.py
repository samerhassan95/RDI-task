import pytest
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
from file_api.models import PDFFile
from PyPDF2 import PdfReader


@pytest.mark.django_db
def test_pdf_file_model():
    # Create a simple PDF in memory
    pdf_data = BytesIO()
    pdf_data.write(b"%PDF-1.4\n%...%")  # Add valid PDF data here
    pdf_data.seek(0)

    # Create SimpleUploadedFile
    pdf_file = SimpleUploadedFile("test.pdf", pdf_data.read(), content_type="application/pdf")

    # Create PDFFile instance
    pdf_instance = PDFFile.objects.create(
        file=pdf_file,
        location='pdfs/test.pdf',
        page_count=1,
        page_width=612.0,
        page_height=792.0
    )

    assert pdf_instance.file.name.startswith('pdfs/')
    assert pdf_instance.location == 'pdfs/test.pdf'
    assert pdf_instance.page_count == 1
    assert pdf_instance.page_width == 612.0
    assert pdf_instance.page_height == 792.0
