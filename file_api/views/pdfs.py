from rest_framework import viewsets
from ..models import PDFFile
from file_api.serializers import PDFFileSerializer
from ..utils.pdfs_utils import extract_pdf_metadata

class PDFFileViewSet(viewsets.ModelViewSet):
    queryset = PDFFile.objects.all()
    serializer_class = PDFFileSerializer

    def perform_create(self, serializer):
        pdf_file = serializer.save(location=serializer.validated_data['file'].name)
        metadata = extract_pdf_metadata(pdf_file.file.path)
        pdf_file.page_count = metadata['page_count']
        pdf_file.page_width = metadata['page_width']
        pdf_file.page_height = metadata['page_height']
        pdf_file.save()
