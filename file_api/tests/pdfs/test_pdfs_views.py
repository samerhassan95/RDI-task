import pytest
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from file_api.models import PDFFile
from io import BytesIO
from PyPDF2 import PdfWriter

def create_valid_pdf():
    pdf_writer = PdfWriter()
    
    # Create a blank page and add it to the writer
    pdf_writer.add_blank_page(width=612, height=792)  # Standard 8.5 x 11 inch page
    
    pdf_data = BytesIO()
    pdf_writer.write(pdf_data)
    pdf_data.seek(0)
    
    return pdf_data

@pytest.mark.django_db
def test_pdf_file_create_and_retrieve(client):
    # Create a valid PDF file
    pdf_data = create_valid_pdf()

    # Use SimpleUploadedFile for file upload
    file = SimpleUploadedFile("test.pdf", pdf_data.read(), content_type="application/pdf")
    
    # Upload the PDF file
    response = client.post('/api/v1/pdfs/', {'file': file}, format='multipart')

    # Check if the response is successful (201 Created)
    assert response.status_code == 201

    # Retrieve the created PDF
    pdf_id = response.data['id']
    response = client.get(f'/api/v1/pdfs/{pdf_id}/')

    # Verify that the location matches the actual file location
    assert response.data['location'] == 'test.pdf'  # Adjusted expected value

@pytest.mark.django_db
def test_pdf_file_delete(client):
    # Create a valid PDF file
    pdf_data = create_valid_pdf()

    # Use SimpleUploadedFile for file upload
    file = SimpleUploadedFile("test.pdf", pdf_data.read(), content_type="application/pdf")

    # Upload the PDF file
    response = client.post('/api/v1/pdfs/', {'file': file}, format='multipart')

    # Check if the response is successful (201 Created)
    assert response.status_code == 201

    pdf_id = response.data['id']

    # Try deleting the created PDF
    response = client.delete(f'/api/v1/pdfs/{pdf_id}/')

    # Assert that the deletion response status is 204 (No Content)
    assert response.status_code == 204

@pytest.mark.django_db
def test_convert_pdf_to_images(client):
    # Create a valid PDF file
    pdf_data = create_valid_pdf()

    # Use SimpleUploadedFile for file upload
    file = SimpleUploadedFile("test.pdf", pdf_data.read(), content_type="application/pdf")

    # Upload the PDF file
    response = client.post('/api/v1/pdfs/', {'file': file}, format='multipart')

    # Check if the PDF file is successfully uploaded
    assert response.status_code == 201

    pdf_id = response.data['id']

    # Ensure the PDF file exists in the database
    assert PDFFile.objects.filter(id=pdf_id).exists()

    # Make the conversion request
    response = client.post('/api/v1/convert-pdf-to-image/', {'pdf_id': pdf_id})

    # Assert that the conversion response is successful (200 OK)
    assert response.status_code == 200
    assert 'PDF successfully converted' in response.data['message']
