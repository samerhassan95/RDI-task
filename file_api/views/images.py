from rest_framework import viewsets
from rest_framework.response import Response
from ..models import ImageFile
from serializers import ImageFileSerializer
from ..utils.images_utils import extract_image_metadata

class ImageFileViewSet(viewsets.ModelViewSet):
    queryset = ImageFile.objects.all()
    serializer_class = ImageFileSerializer

    def perform_create(self, serializer):
        image_file = serializer.save(location=serializer.validated_data['file'].name)
        metadata = extract_image_metadata(image_file.file.path)
        image_file.width = metadata['width']
        image_file.height = metadata['height']
        image_file.channels = metadata['channels']
        image_file.save()
