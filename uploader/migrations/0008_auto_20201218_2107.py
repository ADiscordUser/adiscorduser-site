# Generated by Django 3.1.3 on 2020-12-19 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uploader', '0007_auto_20201218_1709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='media_type',
            field=models.TextField(choices=[('image', 'image'), ('video', 'video')]),
        ),
    ]