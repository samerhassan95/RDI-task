from ..models import PDFFile
from file_api.serializers import PDFFileSerializer
from ..utils.pdfs_utils import extract_pdf_metadata
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

class PDFFileViewSet(viewsets.ModelViewSet):
    queryset = PDFFile.objects.all()
    serializer_class = PDFFileSerializer

    def perform_create(self, serializer):
        try:
            pdf_file = serializer.save(location=serializer.validated_data['file'].name)
            metadata = extract_pdf_metadata(pdf_file.file.path)
            pdf_file.page_count = metadata['page_count']
            pdf_file.page_width = metadata['page_width']
            pdf_file.page_height = metadata['page_height']
            pdf_file.save()
        except ValueError as e:
            raise ValidationError({"error": str(e)})

    def perform_update(self, serializer):
        try:
            pdf_file = serializer.save()
            if 'file' in serializer.validated_data:
                # Update metadata if a new file is uploaded
                pdf_file.location = serializer.validated_data['file'].name
                metadata = extract_pdf_metadata(pdf_file.file.path)
                pdf_file.page_count = metadata['page_count']
                pdf_file.page_width = metadata['page_width']
                pdf_file.page_height = metadata['page_height']
                pdf_file.save()
        except ValueError as e:
            raise ValidationError({"error": str(e)})
        

    def retrieve(self, request, pk=None):
        try:
            pdf = self.get_object()
            metadata = {
                'id': pdf.id,
                'location': pdf.location,
                'page_count': pdf.page_count,
                'page_width': pdf.page_width,
                'page_height': pdf.page_height
            }
            return Response(metadata, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
