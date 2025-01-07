from ..models import PDFFile,ImageFile
from file_api.serializers import PDFFileSerializer
from ..utils.pdfs_utils import extract_pdf_metadata
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from pdf2image import convert_from_path
from pathlib import Path
import shutil ,os

class PDFFileViewSet(viewsets.ModelViewSet):
    # queryset = PDFFile.objects.filter(converted_to_images=False)  # Exclude converted PDFs
    queryset = PDFFile.objects.all()
    serializer_class = PDFFileSerializer

    def perform_create(self, serializer):#### upload pdf ####
        try:
            pdf_file = serializer.save(location=serializer.validated_data['file'].name)
            metadata = extract_pdf_metadata(pdf_file.file.path)
            pdf_file.page_count = metadata['page_count']
            pdf_file.page_width = metadata['page_width']
            pdf_file.page_height = metadata['page_height']
            pdf_file.save()
        except ValueError as e:
            raise ValidationError({"error": str(e)})

    def perform_update(self, serializer):#### update pdf ####
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
        

    def retrieve(self, request, pk=None):#### get pdf details ####
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


#### convert pdf to image ####

class ConvertPDFToImageView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # Validate 'pdf_id' field in request
            pdf_id = request.data.get('pdf_id')
            if not pdf_id:
                raise ValidationError({'error': 'The "pdf_id" field is required.'})

            # Fetch the PDF from the database
            pdf_file = PDFFile.objects.get(id=pdf_id)
            pdf_path = pdf_file.file.path

            if not os.path.exists(pdf_path):
                raise ValidationError({'error': 'The specified PDF file does not exist on the server.'})

            # Prepare the destination directory for the PDF
            destination_dir = Path('media/images')
            destination_dir.mkdir(parents=True, exist_ok=True)

            # Move the PDF file to the new location (from /pdfs to /images)
            new_pdf_path = destination_dir / Path(pdf_file.file.name).name
            shutil.move(pdf_path, new_pdf_path)

            # Update the PDFFile model to reflect the new location
            pdf_file.location = f'images/{Path(pdf_file.file.name).name}'
            pdf_file.save()

            # Return a success response
            return Response({'message': 'PDF converted and moved to images successfully.'}, status=status.HTTP_200_OK)

        except ValidationError as ve:
            # Return validation errors
            return Response({'error': str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Handle unexpected errors
            return Response({'error': f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
