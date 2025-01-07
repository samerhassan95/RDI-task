from rest_framework import status, viewsets
from rest_framework.response import Response
from ..models import ImageFile
from file_api.serializers import ImageFileSerializer
from ..utils.images_utils import extract_image_metadata
from rest_framework.exceptions import ValidationError
import os

class ImageFileViewSet(viewsets.ModelViewSet):
    queryset = ImageFile.objects.all()
    serializer_class = ImageFileSerializer

    def perform_create(self, serializer):
        try:
            image_file = serializer.save(location=serializer.validated_data['file'].name)
            metadata = extract_image_metadata(image_file.file.path)
            image_file.width = metadata['width']
            image_file.height = metadata['height']
            image_file.channels = metadata['channels']
            image_file.save()
        except ValueError as e:
            raise ValidationError({"error": str(e)})



    def perform_update(self, serializer):
        try:
            # Get the existing instance
            instance = self.get_object()

            # Check if a new file is being uploaded
            new_file = serializer.validated_data.get('file', None)
            if new_file and instance.file and os.path.isfile(instance.file.path):
                # Remove the old file
                os.remove(instance.file.path)

            # Save the new data and update metadata if file has changed
            updated_image_file = serializer.save(location=new_file.name if new_file else instance.location)
            
            if new_file:
                metadata = extract_image_metadata(updated_image_file.file.path)
                updated_image_file.width = metadata['width']
                updated_image_file.height = metadata['height']
                updated_image_file.channels = metadata['channels']
                updated_image_file.save()
        except ValueError as e:
            raise ValidationError({"error": str(e)})

    def retrieve(self, request, pk=None):
        try:
            image = self.get_object()
            metadata = {
                'id': image.id,
                'location': image.location,
                'width': image.width,
                'height': image.height,
                'channels': image.channels
            }
            return Response(metadata, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
