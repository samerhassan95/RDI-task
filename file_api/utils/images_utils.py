from PIL import Image

def extract_image_metadata(image_path):
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            channels = len(img.getbands())
            return {
                'width': width,
                'height': height,
                'channels': channels
            }
    except Exception as e:
        raise ValueError(f"Error extracting image metadata: {e}")


