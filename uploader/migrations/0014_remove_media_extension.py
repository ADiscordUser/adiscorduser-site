# Generated by Django 3.1.4 on 2020-12-28 00:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uploader', '0013_media_extension'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='media',
            name='extension',
        ),
    ]
