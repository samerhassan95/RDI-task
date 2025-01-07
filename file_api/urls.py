from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.images import ImageFileViewSet, RotateImageView
from .views.pdfs import PDFFileViewSet, ConvertPDFToImageView

# Use DefaultRouter for automatic URL generation for ViewSets
router = DefaultRouter()
router.register(r'images', ImageFileViewSet, basename='image')
router.register(r'pdfs', PDFFileViewSet, basename='pdf')



custom_urlpatterns = [
    path('rotate/', RotateImageView.as_view(), name='rotate-image'),
    path('convert-pdf-to-image/', ConvertPDFToImageView.as_view(), name='convert-pdf-to-image'),
]

# Combine router URLs with custom URLs
urlpatterns = router.urls + custom_urlpatterns
