import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from file_api.serializers import PDFFileSerializer
from io import BytesIO

@pytest.mark.django_db
def test_pdf_file_serializer():
    # Create a simple PDF in memory
    pdf_data = BytesIO()
    pdf_data.write(b"%PDF-1.4\n%...%")  # Add valid PDF data here
    pdf_data.seek(0)

    # Create SimpleUploadedFile
    pdf_file = SimpleUploadedFile("test.pdf", pdf_data.read(), content_type="application/pdf")

    data = {
        'file': pdf_file,
        'location': 'pdfs/test.pdf',
        'page_count': 1,
        'page_width': 612.0,
        'page_height': 792.0
    }

    serializer = PDFFileSerializer(data=data)
    assert serializer.is_valid(), f"Validation failed: {serializer.errors}"
    pdf_instance = serializer.save()

    assert pdf_instance.file.name.startswith('pdfs/')
    assert pdf_instance.location == 'pdfs/test.pdf'
    assert pdf_instance.page_count == 1
    assert pdf_instance.page_width == 612.0
    assert pdf_instance.page_height == 792.0
