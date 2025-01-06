from rest_framework import serializers
from .models import ImageFile, PDFFile

##### Image Serializer #####
class ImageFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageFile
        fields = ['id', 'file', 'uploaded_at', 'location', 'width', 'height', 'channels']


##### PDF Serializer #####
class PDFFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PDFFile
        fields = ['id', 'file', 'uploaded_at', 'location', 'page_count', 'page_width', 'page_height']
