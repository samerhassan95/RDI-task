from django.urls import path, include
from rest_framework.routers import DefaultRouter
from file_api.views.images import ImageFileViewSet
from file_api.views.pdfs import PDFFileViewSet

# Use DefaultRouter for automatic URL generation for ViewSets
router = DefaultRouter()
router.register(r'images', ImageFileViewSet, basename='image')
router.register(r'pdfs', PDFFileViewSet, basename='pdf')




urlpatterns = router.urls 
