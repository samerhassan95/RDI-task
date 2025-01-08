import pytest
from file_api.models import ImageFile

@pytest.mark.django_db
def test_image_file_model_creation():
    image = ImageFile.objects.create(file='images/test.jpg', location='images/test.jpg', width=1024, height=768, channels=3)
    assert image.file.name == 'images/test.jpg'
    assert image.location == 'images/test.jpg'
    assert image.width == 1024
    assert image.height == 768
    assert image.channels == 3
