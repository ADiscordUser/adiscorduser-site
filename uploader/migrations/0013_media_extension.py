# Generated by Django 3.1.4 on 2020-12-27 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uploader', '0012_auto_20201220_2035'),
    ]

    operations = [
        migrations.AddField(
            model_name='media',
            name='extension',
            field=models.CharField(default='sexy', max_length=4),
            preserve_default=False,
        ),
    ]
