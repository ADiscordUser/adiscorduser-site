# Generated by Django 3.0.7 on 2020-07-18 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uploader', '0002_auto_20200704_0044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='creation',
            field=models.DateTimeField(),
        ),
    ]