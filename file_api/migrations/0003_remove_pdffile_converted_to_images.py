# Generated by Django 5.1.4 on 2025-01-07 19:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('file_api', '0002_pdffile_converted_to_images'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pdffile',
            name='converted_to_images',
        ),
    ]
