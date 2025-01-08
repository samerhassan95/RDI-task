import io
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from file_api.serializers import ImageFileSerializer
from file_api.models import ImageFile
from PIL import Image

@pytest.mark.django_db
def test_image_file_serializer():
    # Create a simple image in memory (valid .jpg content)
    image_data = io.BytesIO()
    # Generate a small image in memory (using PIL or any other method)
    img = Image.new('RGB', (100, 100), color = (73, 109, 137))
    img.save(image_data, format='JPEG')
    image_data.seek(0)

    # Create the SimpleUploadedFile object
    image_file = SimpleUploadedFile("test.jpg", image_data.read(), content_type="image/jpeg")

    data = {
        'file': image_file,
        'location': 'images/test.jpg',
        'width': 1024,
        'height': 768,
        'channels': 3
    }

    # Initialize the serializer with the data
    serializer = ImageFileSerializer(data=data)

    # Run validation
    assert serializer.is_valid(), f"Validation failed: {serializer.errors}"

    # Save the instance if validation passed
    image_instance = serializer.save()

    # Assertions to ensure proper values
    # Check that the file name starts with 'images/test' (due to auto-renaming by Django)
    assert image_instance.file.name.startswith('images/test')
    assert image_instance.location == 'images/test.jpg'
    assert image_instance.width == 1024
    assert image_instance.height == 768
    assert image_instance.channels == 3
