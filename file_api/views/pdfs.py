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
from PIL import Image
from ..utils.images_utils import extract_image_metadata

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
        

         # Delete PDF and media file
    def destroy(self, request, *args, **kwargs): 
        try:
            # Get the object to be deleted
            instance = self.get_object()

            # Delete associated files
            pdf_path = instance.file.path
            if os.path.isfile(pdf_path):
                os.remove(pdf_path)

            # Check for associated image folder and delete it
            pdf_images_dir = Path(f'media/pdf_images/{instance.id}')
            if pdf_images_dir.exists() and pdf_images_dir.is_dir():
                shutil.rmtree(pdf_images_dir)

            # Delete the database record
            response = super().destroy(request, *args, **kwargs)
            return response
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#### convert pdf to image ####



class ConvertPDFToImageView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # Get the 'pdf_id' from the request
            pdf_id = request.data.get('pdf_id')
            if not pdf_id:
                raise ValidationError({'error': 'The "pdf_id" field is required.'})

            # Fetch the PDFFile instance
            pdf_file = PDFFile.objects.get(id=pdf_id)
            pdf_path = pdf_file.file.path

            # Prepare destination folder for the PDF and images
            pdf_images_dir = Path(f'media/pdf_images/{pdf_id}')
            pdf_images_dir.mkdir(parents=True, exist_ok=True)

            # Convert the PDF to images
            images = convert_from_path(pdf_path, poppler_path=r'C:\poppler-24.08.0\Library\bin')
            for i, image in enumerate(images):
                # Save each image in the `pdf_images` folder
                image_output_path = pdf_images_dir / f"page_{i + 1}.jpg"
                image.save(image_output_path, 'JPEG')

                # Extract metadata from the image
                metadata = extract_image_metadata(str(image_output_path))

                # Save the image in the database with metadata
                ImageFile.objects.create(
                    file=f'pdf_images/{pdf_id}/page_{i + 1}.jpg',
                    location=str(image_output_path),
                    width=metadata['width'],
                    height=metadata['height'],
                    channels=metadata['channels']
                )

            # Move the PDF file to the `pdf_images` folder
            pdf_destination_path = pdf_images_dir / Path(pdf_file.file.name).name
            shutil.move(pdf_path, pdf_destination_path)

            # Clean up the PDFFile entry and associated file
            pdf_file.delete()

            return Response({
                'message': 'PDF successfully converted to images, metadata extracted, and deleted from the /pdfs endpoint.'
            }, status=status.HTTP_200_OK)

        except ValidationError as ve:
            return Response({'error': str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except PDFFile.DoesNotExist:
            return Response({'error': f'PDF with ID {pdf_id} does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
