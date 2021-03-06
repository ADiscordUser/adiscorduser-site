# Generated by Django 3.1.4 on 2021-01-03 02:41

from django.db import migrations, models
import uploader.models
import uploader.storage
import uploader.validation


class Migration(migrations.Migration):

    dependencies = [
        ('uploader', '0014_remove_media_extension'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='media',
            field=models.FileField(storage=uploader.storage.MediaStorage, upload_to=uploader.models.determine_media_path, validators=[uploader.validation.media_type_validator]),
        ),
    ]