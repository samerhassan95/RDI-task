import pytest
import io
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from file_api.models import ImageFile
from PIL import Image


@pytest.mark.django_db
def test_image_file_upload():
    client = APIClient()
    
    # Create a valid in-memory image
    image_data = io.BytesIO()
    from PIL import Image
    img = Image.new('RGB', (100, 100), color=(73, 109, 137))
    img.save(image_data, format='JPEG')
    image_data.seek(0)

    # Create the SimpleUploadedFile object with valid image content
    image_file = SimpleUploadedFile("test.jpg", image_data.read(), content_type="image/jpeg")

    # Test file upload
    response = client.post('/api/v1/images/', {'file': image_file})

    # Debug: Print the response content
    print(response.data)

    # Check the response status
    assert response.status_code == 201


@pytest.mark.django_db
def test_image_retrieve():
    client = APIClient()

    # Create an image file
    image = ImageFile.objects.create(file='images/test.jpg', width=800, height=600, channels=3)

    # Test retrieving the image metadata
    response = client.get(f'/api/v1/images/{image.id}/')
    assert response.status_code == 200
    assert response.data['width'] == 800
    assert response.data['height'] == 600
    assert response.data['channels'] == 3

@pytest.mark.django_db
def test_image_delete():
    client = APIClient()

    # Create an image file
    image = ImageFile.objects.create(file='images/test.jpg')

    # Test deleting the image
    response = client.delete(f'/api/v1/images/{image.id}/')
    assert response.status_code == 204
    assert not ImageFile.objects.filter(id=image.id).exists()



@pytest.mark.django_db
def test_rotate_image(monkeypatch, tmpdir):
    client = APIClient()

    # Mock image creation
    img_path = tmpdir.join("test.jpg")
    with Image.new('RGB', (100, 100)) as img:
        img.save(img_path)

    # Create an image file in the database
    with open(img_path, 'rb') as f:
        image_file = SimpleUploadedFile('test.jpg', f.read(), content_type='image/jpeg')
        response = client.post('/api/v1/images/', {'file': image_file})
        assert response.status_code == 201

    image_id = response.data['id']

    # Test image rotation
    rotate_response = client.post('/api/v1/rotate/', {'image_id': image_id, 'angle': 90})
    assert rotate_response.status_code == 200
    assert rotate_response.data['message'] == 'Image rotated successfully.'

    # Verify the image was rotated (optional: confirm dimensions if rotation changes them)
    rotated_image = ImageFile.objects.get(id=image_id)
    with Image.open(rotated_image.file.path) as img:
        assert img.size == (100, 100)  # Dimensions should remain same since rotation is 90° with expand=True

