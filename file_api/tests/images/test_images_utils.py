import pytest
from file_api.utils.images_utils import extract_image_metadata
from PIL import Image
import os

@pytest.mark.django_db
def test_extract_image_metadata(tmpdir):
    # Create a temporary image
    img_path = tmpdir.join("test.jpg")
    with Image.new('RGB', (200, 300)) as img:
        img.save(img_path)

    # Extract metadata
    metadata = extract_image_metadata(str(img_path))

    # Validate the metadata
    assert metadata['width'] == 200
    assert metadata['height'] == 300
    assert metadata['channels'] == 3  # RGB has 3 channels

@pytest.mark.django_db
def test_extract_image_metadata_invalid_file(tmpdir):
    # Create a non-image file
    invalid_file_path = tmpdir.join("test.txt")
    with open(invalid_file_path, 'w') as f:
        f.write("This is not an image")

    # Test extracting metadata from an invalid file
    with pytest.raises(ValueError, match="Error extracting image metadata"):
        extract_image_metadata(str(invalid_file_path))
