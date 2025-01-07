from rest_framework import serializers
from .models import ImageFile, PDFFile

##### Image Serializer #####
class ImageFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageFile
        fields = ['id', 'file', 'uploaded_at', 'location', 'width', 'height', 'channels']

    def validate_file(self, file):
        if not file.name.lower().endswith(('.png', '.jpg', '.jpeg')):
            raise serializers.ValidationError("Invalid file type. Only PNG, JPG, and JPEG are allowed.")
        if file.size > 5 * 1024 * 1024:  # 5MB limit
            raise serializers.ValidationError("File size exceeds the 5MB limit.")
        return file

##### PDF Serializer #####
class PDFFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PDFFile
        fields = ['id', 'file', 'uploaded_at', 'location', 'page_count', 'page_width', 'page_height']

    def validate_file(self, file):
        if not file.name.lower().endswith('.pdf'):
            raise serializers.ValidationError("Invalid file type. Only PDF files are allowed.")
        if file.size > 10 * 1024 * 1024:  # 10MB limit
            raise serializers.ValidationError("File size exceeds the 10MB limit.")
        return file