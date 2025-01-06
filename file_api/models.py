from django.db import models

# Create your models here.

#### Image Model ####
class ImageFile(models.Model):
    file = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    channels = models.IntegerField(null=True, blank=True) 

    def __str__(self):
        return self.file.name
    

#### PDF Model ####
class PDFFile(models.Model):
    file = models.FileField(upload_to='pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    page_count = models.IntegerField(null=True, blank=True)
    page_width = models.FloatField(null=True, blank=True)
    page_height = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.file.name
    

